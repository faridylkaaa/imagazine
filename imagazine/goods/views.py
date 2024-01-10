from django.shortcuts import render
from django.views import View

# Create your views here.
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'goods/index.html')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная'
        context["goods"] = 1
        return context