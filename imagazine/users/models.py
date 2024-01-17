from django.db import models
from django.contrib.auth.models import AbstractUser
from imagazine.goods.models import Goods


class User(AbstractUser):
    username = models.TextField(blank=True, null=True, unique=False)
    photo = models.ImageField(blank=True, null=True, upload_to='images/', default='images/img_avatar.png', verbose_name="Фото")
    date_of_birth = models.DateField()
    favor = models.ManyToManyField(Goods, blank=True, null=True, related_name='user')