from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Game, Console

# Create your views here.
class GamesIndexView(ListView):
    paginate_by = 8
    template_name = 'goods/index.html'
    context_object_name = 'games'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Игры'
        return context
    
    def get_queryset(self):
        return Game.objects.all().order_by('-count')
    
class ProfileGameView(DetailView):
    model = Game
    template_name = 'goods/profile.html'
    context_object_name = 'game'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        content = super().get_context_data(**kwargs)
        content['title'] = 'Игра' + content['game'].name
        content['cat'] = '/'.join([name.name for name in content['game'].category.all()])
        return content