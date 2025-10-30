from typing import Any
from django.http import Http404
from django.views.generic import ListView, DetailView
from book.models import BooksCategories, BooksRead
from book.utils import q_search
from django.db.models.query import QuerySet
import requests
from app.settings import GET_PAGE_BOOK
# Create your views here.
class CatalogView(ListView):
    template_name = 'book/book.html'
    model = BooksRead
    paginate_by = 6
    context_object_name = 'books'
    allow_empty = True
    
    
    def get_queryset(self):
        books_slug = self.kwargs.get('slug_url')
        book_search = self.request.GET.get('books_search')
        rating = self.request.GET.get('ratings')
        year = self.request.GET.get('year')
        
        if books_slug == 'all':
            books = super().get_queryset().order_by('id')
                
        elif book_search:
            books = q_search(book_search)
                        
        else:
            books = super().get_queryset().filter(category__slug=books_slug)
        
        if rating:
            if rating == 'one':
                books = books.filter(ratings__gt=4.5)
            else:
                books = books.filter(ratings__gt=4.0)
        
        if year:
            if year == 'one':
                books = books.filter(reliz_year__gt=1800, reliz_year__lt=1900)
            if year == 'two':
                books = books.filter(reliz_year__gt=1900,reliz_year__lt=2000)
            if year == 'three':
                books = books.filter(reliz_year__gt=2000)
              
        return books
     
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        catalog = BooksCategories.objects.all().order_by('id')
        context['catalog'] = catalog
        context['slug_url'] = self.kwargs.get('slug_url')
        return context
 

    
class ReadBook(DetailView):
    template_name = 'book/book_read.html'
    slug_url_kwarg = 'book_slug'
    context_object_name = 'book'
    
    def _fetch_page_from_api(self, book_id, page_number):
        """Отправка и полуение данных"""
        try:
            payload = {
                'page' : page_number,
                'book_id' : book_id,
            }
            response = requests.post(GET_PAGE_BOOK,
                                    json = payload,
                                    timeout=10).json()
            return response['content'] if response['cod'] == '3001' else None
        except Exception as e:
            return None
        
    def get_page(self, obj, page):
        """Функция для получения данных страницы от фастапи"""
        if not obj or not obj.book_id:
            return obj
        page_number = 1 if page == None else int(page)
        
        if page_number < 1 or page_number > obj.book_lists:
            return obj
        obj.book_content = self._fetch_page_from_api(obj.book_id, str(page_number))
        obj.book_page = page_number
        obj.book_read_percent = round((page_number * 100) / obj.book_lists, 2)
        return obj
         
    def get_object(self, queryset: QuerySet[Any] | None = ...) :
        
        page = self.request.GET.get('page', None)
        like = self.request.GET.get('like', None)
        try:
            book = BooksRead.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
            if like == '1':
                BooksRead.objects.filter(pk=book.pk).update(
                    likes = book.likes + 1,
                )
            
            return  self.get_page(book, page)         
        except Exception as e:
            raise Http404(f'Книга не найдена')
        
                
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Читать'
        return context
    
  