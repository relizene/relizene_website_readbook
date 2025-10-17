from django.views.generic import  TemplateView
from main.utils import find_temprature, find_temprature_coord

# Create your views here.
class Indexview(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        city = self.request.GET.get('city_name', None)
        lat = self.request.GET.get('lat', None)
        lon = self.request.GET.get('lon', None)
        
        if city:
            data = find_temprature(city=city)
            context['data'] = data
        if lat and lon:
            data = find_temprature_coord(lat, lon)
            context['data'] = data
            
        
        context['title'] = 'Home - Главная страница'
    
        return context
