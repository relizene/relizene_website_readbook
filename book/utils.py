from book.models import BooksRead
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank



def q_search(query):
    vector = SearchVector('name', 'description', config='russian')
    query = SearchQuery(query, search_type='phrase')
    
    result = (
        BooksRead.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0.01)
        .order_by('-rank'))
    
    return result
    