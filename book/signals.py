from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BooksRead, BooksCategories

@receiver(post_save, sender=BooksRead)
@receiver(post_delete, sender=BooksRead)
def update_category_count(sender, instance, **kwargs):
    category = instance.category
    category.books_count = category.booksread_set.count()
    category.save()