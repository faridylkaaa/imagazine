from django_filters import FilterSet, filters
from .models import Game, Console
import django_filters

def filter(queryset, name, value):
    if value == True:
        return queryset.filter(count__gt=1)
    return queryset.filter(count__lt=1)

class GameFilter(FilterSet):
    def __init__(self, *args, **kwargs):
       super(GameFilter, self).__init__(*args, **kwargs)
       self.filters['category'].label="Категория"
       self.filters['compatibility'].label="Совместимость"
       self.filters['developer'].label="Разработчик"
       
    name = filters.CharFilter(label='Название', lookup_expr='icontains')
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt', label='Цена от')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt', label='Цена до')
    avaliable = filters.BooleanFilter(method=filter, label='В наличии', )
    
    class Meta:
        model = Game
        fields = ['name', 'category', 'compatibility', 'developer']
        
class ConsoleFilter(FilterSet):
    def __init__(self, *args, **kwargs):
       super(ConsoleFilter, self).__init__(*args, **kwargs)
       self.filters['model_console'].label="Модель консоли"
       
    name = filters.CharFilter(label='Название', lookup_expr='icontains')
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt', label='Цена от')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt', label='Цена до')
    avaliable = filters.BooleanFilter(method=filter, label='В наличии', )
    
    class Meta:
        model = Console
        fields = ['name', 'model_console']