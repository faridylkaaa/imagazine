from typing import Any
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from imagazine.users.forms import *
from imagazine.users.models import User
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.views.generic.detail import DetailView
from .mixins import RightUserMixin
from django.contrib.auth.mixins import LoginRequiredMixin

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
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uid64': uid, 'token': token})
        current_site = Site.objects.get_current().domain
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты: http://{current_site}{activation_url}',
            'faridylkaaa@yandex.ru',
            [user.email],
            fail_silently=False,
        )
        return redirect(reverse_lazy('users:email_confirmation_sent'))
    
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Пользователь вышел')
        return redirect(reverse_lazy('main'))
    else:
        messages.info(request, 'Вы не авторизованы')
        return redirect(reverse_lazy('users:login'))
    
class ConfirmEmailView(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64)
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            user = None
        
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Почта подтверждена')
            return redirect(reverse_lazy('users:login'))
        else:
            return redirect(reverse_lazy('users:email_not_confirm'))
        
class ProfileUserView(RightUserMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context
    
class DeleteUserView(LoginRequiredMixin, SuccessMessageMixin, RightUserMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_message = 'Пользователь удален'
    login_url = reverse_lazy('users:login')
    success_url = reverse_lazy('main')