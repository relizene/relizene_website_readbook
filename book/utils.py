from book.models import BooksRead
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank



def q_search(query):
    vector = SearchVector('name')
    query = SearchQuery(query)
    
    result = (
        BooksRead.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by('-rank'))
    
    return result
    