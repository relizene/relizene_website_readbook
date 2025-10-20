from django.db import models
import requests
import base64
import os

# Create your models here.
class BooksCategories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Url')
    books_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'book_category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['id']
    def __str__(self) -> str:
        return self.name  
    
class BooksRead(models.Model):
    UPLOAD_STATUS = (
        ('pending', 'В ожидании'),
        ('success', 'успешно'),
        ('error', 'ошибка'),
        ('delete', 'книга удалена')
    )
    
    name = models.CharField(max_length=150, unique=True, verbose_name='Название Книги')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Url')
    author_name = models.CharField(max_length=150,  verbose_name='Автор книги')
    reliz_year = models.CharField(max_length=150,  verbose_name='Год выпуска')
    description = models.TextField(blank=True, null=True, verbose_name='Описание',)
    image = models.ImageField(upload_to='book_images', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(to=BooksCategories, on_delete=models.CASCADE, verbose_name='Категория')
    likes = models.IntegerField(blank=True, null=True, verbose_name='Лайки')
    file = models.FileField(blank=True, null=True, upload_to='book_file', verbose_name='Файл книги в pdf')
    
    #статусы ожидания
    upload_message = models.TextField(blank=True, null=True)
    upload_status = models.CharField(max_length=20, choices=UPLOAD_STATUS, default='pending')
    
    #данные от микросервиса
    book_lists = models.IntegerField(blank=True, null=True, verbose_name='Количество листов')
    book_id = models.CharField(max_length=150, blank=True, null=True, verbose_name='id книги в монго')
       
    class Meta:
        db_table = 'book'
        verbose_name = 'Книги'
        verbose_name_plural = 'Книги'
        ordering = ['id']
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        #Сначала сохраняем обьект чтобы получить file_path
        super().save(*args, **kwargs)
        
        #отправка в микросервис если статус "pending" и есть file
        if self.file and self.upload_status == 'pending':
            self._upload_to_microservice()            
    
    
    def _upload_to_microservice(self):
        """Отправка данных в микросервис"""
        #Получение пути до хранения книги
        file_path = self.file.path if self.file else None
        try:
            if not file_path or not os.path.exists(file_path):
                raise FileNotFoundError(f'Файл не найден: {file_path}')
            
            with open(self.file.path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')
                payload = {
                    'book_name' : self.name,
                    'content' : file_data, 
                }
                response = requests.post(
                    'http://localhost:8000/books-upload',
                    json = payload,
                    timeout = 30
                ).json()
                
                if response['cod'] == '1001':
                    #метод update вместо save во избежании рекурсии
                    BooksRead.objects.filter(pk=self.pk).update(
                        upload_message = 'Успешно загружено в БД',
                        upload_status = 'success',
                        book_lists = int(response['сохраненные страницы']),
                        book_id = response['id_книги'],
                        file = None
                    )
                else:
                    BooksRead.objects.filter(pk=self.pk).update(
                        upload_message = f"Ошибка {response['cod']} {response['message'] }",
                        upload_status = 'error',
                        book_lists = 0,
                        book_id = 0,
                        file = None
                    )
        except Exception as e:
            BooksRead.objects.filter(pk=self.pk).update(
                upload_status = 'error',
                upload_message = f'ошибка: {e}',
                file = None,
            )
        finally:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(f'{file_path}')
                except OSError as e:
                    print(f'Ошибка удалении файла {e}') 
       
        
    
    