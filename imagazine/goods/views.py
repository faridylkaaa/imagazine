from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Game, Console
from .filters import GameFilter, ConsoleFilter
from django.http import Http404
from imagazine.cart.forms import CatrAddForm


# Create your views here.
class GamesIndexView(ListView):
    filterset_class = GameFilter
    paginate_by = 8
    template_name = 'goods/index.html'
    context_object_name = 'games'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Игры'
        context['filterset'] = self.filterset
        return context
    
    def get_queryset(self):
        queryset = Game.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.order_by('-count')
    
class ProfileGameView(DetailView):
    model = Game
    template_name = 'goods/profile.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        content = super().get_context_data(**kwargs)
        content['title'] = content['game'].name
        content['form'] = CatrAddForm
        content['cat'] = '/'.join([name.name for name in content['game'].category.all()])
        return content
    
class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = CatrAddForm
        return render(request, 'goods/category.html', {'form': form})
    
class ConsolesView(ListView):
    context_object_name = 'consoles'
    template_name = 'goods/console.html'
    paginate_by = 8
    filterset_class = ConsoleFilter
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Консоли'
        context['filterset'] = self.filterset
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = Console.objects.all()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.order_by('-count')
    
class ConsoleView(DetailView):
    context_object_name = 'console'
    template_name = 'goods/profile_console.html'
    model = Console
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        content = super().get_context_data(**kwargs)
        content['form'] = CatrAddForm
        content['title'] = content['console'].name
        return content