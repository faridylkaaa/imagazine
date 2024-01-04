from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(blank=True, null=True, upload_to='images/', default=None, verbose_name="Фото")
    date_of_birth = models.DateField()