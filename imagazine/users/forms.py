from django.contrib.auth.forms import AuthenticationForm
from django import forms
from imagazine.users.models import User

class UserAuthForm(AuthenticationForm):
    username = forms.CharField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-floating'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-floating'}))
    
    class Meta:
        model = User
        fields = ['email',
                  'password'
                  ]