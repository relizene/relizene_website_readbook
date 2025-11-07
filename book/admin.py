from email import message
from typing import Any
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
import requests
from book.models import BooksCategories, BooksRead
from django.contrib import messages
from django.http import HttpResponseRedirect
from app.settings import DELETE_BOOK


#admin.site.register(Categories)
#admin.site.register(Products)
def delete_book_from_mongo(modeladmin, request, queryset):
    """Кастомное удаление книги из монго"""
    for book in queryset:
        payload = {
            'id' : book.book_id,
            'pages' : str(book.book_lists),
                   }
        if book.book_id:
            try:
                response = requests.post(DELETE_BOOK, json=payload, timeout=30).json()
                if response['cod'] == '2001':
                    #Полное удаление и страниц и книги
                    BooksRead.objects.filter(pk=book.pk).update(
                        upload_message = f"{response['message']}",
                        upload_status = 'delete',
                        book_lists = 0,
                        book_id = None,
                    )
                    messages.success(request, f"Книга '{book.name}' удалена из MongoDB")
                    
                elif response['cod'] == '2003':
                    #Частичное удаление, страницы удалены, но запись в книге осталась
                    BooksRead.objects.filter(pk=book.pk).update(
                        upload_message = f"{response['message']}",
                        upload_status = 'success',
                        book_lists = 0,
                        book_id = book.book_id,
                    )
                    messages.error(request, f"Книга '{book.name}' не удалена из MongoDB, но страницы все удалились, повторите удаление")
                    
                elif response['cod'] == '2002':
                    #Частичное удаление, страницы удалились в не полном составе и книга поэтому тоже не удаляется
                    BooksRead.objects.filter(pk=book.pk).update(
                        upload_message = f"{response['message']}",
                        upload_status = 'success',
                        book_lists = book.book_lists - int(response['delete_count']),
                        book_id = book.book_id,
                    )
                    messages.error(
                        request, f"Книга '{book.name}' не удалена из MongoDB, страницы удалились в количестве {response['delete_count']}"
                        )
                    
                else:
                    messages.error(request, f"{response['message']}")
                    
            except Exception as e:
                messages.error(request, f"Ошибка при удалении '{book.name}': {str(e)}")
                
        else:
             messages.warning(request, f"Книга '{book.name}' не найдена в MongoDB или еще пока не существует")
             
delete_book_from_mongo.short_description = "🗑️ Удалить выбранные книги из MongoDB"


@admin.register(BooksCategories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'id', 'books_count']
    readonly_fields = ('books_count',)
    
# Register your models here.

@admin.register(BooksRead)
class BooksAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'upload_status', 'book_id']
    
    actions = [delete_book_from_mongo]
    
    def save_model(self, request: HttpRequest, obj, form: ModelForm, change: bool) -> None:
        if change and 'file' in form.changed_data:
            obj.upload_status = 'pending'
            obj.upload_message = ''          
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request: HttpRequest, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        
        readonly_fields =  super().get_readonly_fields(request, obj)
        readonly_fields = ('book_lists','book_id', 'upload_message', 'upload_status',)
        if obj and obj.upload_status == 'success':
            return readonly_fields + ('file',)    
        return readonly_fields
    
    def delete_model(self, request, obj):
            if obj.pk is None:
                messages.warning(request, f'ошибка: {obj.name} к сожалению не найден')
            if obj.book_id:
                payload = {
                    'id' : obj.book_id,
                    'pages' : str(obj.book_lists),
                }
                try:
                    response = requests.post(DELETE_BOOK, json=payload, timeout=30).json()
                    if response['cod'] == '2001':
                        #Полное удаление и страниц и книги и самой записи в постгресс
                        super().delete_model(request, obj)
                    
                    elif response['cod'] == '2003':
                        #Частичное удаление, страницы удалены, но запись в книге осталась, поэтому из постгресс не убираем
                        BooksRead.objects.filter(pk=obj.pk).update(
                        upload_message = f"{response['message']}",
                        upload_status = 'success',
                        book_lists = 0,
                        book_id = obj.book_id,
                        )
                        messages.error(request, 
                                       f"Книга '{obj.name}' не удалена из MongoDB," + 
                                       " но страницы все удалились, повторите удаление")
                    
                    elif response['cod'] == '2002':
                        #Частичное удаление, страницы удалились в не полном составе и книга поэтому тоже не удаляется
                        BooksRead.objects.filter(pk=obj.pk).update(
                        upload_message = f"{response['message']}",
                        upload_status = 'success',
                        book_lists = obj.book_lists - int(response['delete_count']),
                        book_id = obj.book_id,
                        )
                        messages.error(
                        request, f"Книга '{obj.name}' не удалена из MongoDB, страницы удалились" +
                                        f" в количестве {response['delete_count']}"
                        )
                    else:
                        messages.error(request, f"ошибка: {response['message']}")
                        
                except Exception as e:
                    messages.error(request, f'ошибка удаления из монго DB: {str(e)}')
            else:
                super().delete_model(request, obj)