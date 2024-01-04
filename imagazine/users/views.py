from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from imagazine.users.forms import *
from imagazine.users.models import User
from django.contrib.auth import logout
from django.contrib import messages

# Create your views here.
class LoginUserView(SuccessMessageMixin, LoginView):
    success_url = reverse_lazy('main')
    login_url = reverse_lazy('users:login')
    success_message = 'Вы авторизованы'
    form_class = UserAuthForm
    template_name = 'users/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Вход'
        return context
    
    
class CreateUserView(SuccessMessageMixin, CreateView):
    success_message = 'Пользователь создан'
    success_url = reverse_lazy('users:login')
    form_class = UserCreateForm
    # fields = ['username', 'password1', 'password2', 'photo', 'date_of_birth']
    template_name = 'users/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация'
        return context
    
def logout_user(request, *args, **kwargs):
    logout(request)
    messages.success(request, 'Пользователь вышел')
    return redirect(reverse_lazy('main'))