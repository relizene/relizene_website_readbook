from django.urls import path
from book import views
app_name = 'book'

urlpatterns = [
    path('<slug:slug_url>', views.CatalogView.as_view(), name='book'),
]
