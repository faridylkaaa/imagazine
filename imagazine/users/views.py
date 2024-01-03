from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from imagazine.users.forms import *
from imagazine.users.models import User

# Create your views here.
class LoginUserView(SuccessMessageMixin, LoginView):
    success_url = reverse_lazy('main')
    success_message = 'Вы авторизованы'
    form_class = UserAuthForm
    template_name = 'users/login.html'
    
class CreateUserView(SuccessMessageMixin, CreateView):
    success_message = 'Пользователь создан'
    success_url = reverse_lazy('users:login')
    model = User
    fields = ['username', 'password1', 'password2', 'photo', 'date_of_birth']
    template_name = ''