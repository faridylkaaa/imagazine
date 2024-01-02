from django.views import View
from django.shortcuts import render

class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Главная'
        return context
    