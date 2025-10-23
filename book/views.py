from typing import Any
from django.http import Http404
from django.views.generic import ListView, DetailView
from book.models import BooksCategories, BooksRead
from book.utils import q_search
from django.db.models.query import QuerySet
import requests

# Create your views here.
class CatalogView(ListView):
    template_name = 'book/book.html'
    model = BooksRead
    paginate_by = 3
    context_object_name = 'books'
    allow_empty = False
    
    
    def get_queryset(self):
        books_slug = self.kwargs.get('slug_url')
        book_search = self.request.GET.get('books_search')
        
        if books_slug == 'all':
            books = super().get_queryset().order_by('id')            
        elif book_search:
            books = q_search(book_search)
            if not books:
                raise Http404()           
        else:
            books = super().get_queryset().filter(category__slug=books_slug)       
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
            response = requests.post('http://localhost:8000/get_page',
                                    json = payload,
                                    timeout=10).json()
            return response['content'] if response['cod'] == '3001' else None
        except Exception as e:
            return None
        
    
    def get_page(self, obj, page):
        """Функция для получения данных страницы от фастапи"""
        if not obj or not obj.book_id:
            raise Http404(f'к сожалению данной книги нет или книга не загружена')
        page_number = 1 if page == None else int(page)
        
        if page_number < 1 or page_number > obj.book_lists:
            raise Http404(f'к сожалению данной страницы нету.')
        obj.book_content = self._fetch_page_from_api(obj.book_id, str(page_number))
        obj.book_page = page_number
        obj.book_read_percent = round((page_number * 100) / obj.book_lists, 2)
        return obj
        
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) :
        try:
            book = BooksRead.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
            page = self.request.GET.get('page', None)
            return  self.get_page(book, page)         
        except Exception as e:
            raise Http404(f'Книга не найдена')
        
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Читать'
        return context
    
  