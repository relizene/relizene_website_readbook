from django.urls import path
from book import views
app_name = 'book'

urlpatterns = [
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:slug_url>', views.CatalogView.as_view(), name='book'),
    path('book_read/<slug:book_slug>', views.ReadBook.as_view(), name='read')
]
