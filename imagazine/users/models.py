from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.TextField(blank=True, null=True, unique=False)
    photo = models.ImageField(blank=True, null=True, upload_to='images/', default='images/img_avatar.png', verbose_name="Фото")
    date_of_birth = models.DateField()