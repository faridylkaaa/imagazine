from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from imagazine.users.models import User

class UserAuthForm(AuthenticationForm):
    username = forms.CharField(label='Почта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['email',
                  'password'
                  ]
        
class UserCreateForm(UserCreationForm):
    email = forms.CharField(label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'class': 'form-control'}))
    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['email',
                  'date_of_birth',
                  'photo', 
                  'password1', 'password2']