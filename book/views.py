from typing import Any
from django.views.generic import ListView, TemplateView
from book.models import BooksCategories, BooksRead

# Create your views here.
class CatalogView(ListView):
    template_name = 'book/book.html'
    model = BooksRead
    paginate_by = 6
    context_object_name = 'books'
    
    
    def get_queryset(self):
        books_slug = self.kwargs.get('slug_url')
        
        if books_slug == 'all':
            books = super().get_queryset().order_by('-id')
            return books
        else:
            books = super().get_queryset().filter(category__slug=books_slug)
            return books
    
    
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        catalog = BooksCategories.objects.all().order_by('id')
        context['catalog'] = catalog
        context['slug_url'] = self.kwargs.get('slug_url')
        return context
    
    

    