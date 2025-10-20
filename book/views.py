from typing import Any
from django.views.generic import ListView
from book.models import BooksCategories, BooksRead
from book.utils import q_search

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
        else:
            books = super().get_queryset().filter(category__slug=books_slug)       
        return books
    
    
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        catalog = BooksCategories.objects.all().order_by('id')
        context['catalog'] = catalog
        context['slug_url'] = self.kwargs.get('slug_url')
        return context
    
    

    