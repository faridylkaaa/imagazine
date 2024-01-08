from django.db import models

# Create your models here.
class CategoryGame(models.Model):
    name = models.TextField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
class Developer(models.Model):
    name = models.TextField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
class Status(models.Model):
    cat = (
    ('LOT', 'В наличии'),
    ('FEW', 'Осталось мало'),
    ('NOT_AV', 'Нет в наличии')
    )
    name = models.CharField(max_length=25, choices=cat)
    def __str__(self) -> str:
        return self.name
    
class ModelConsole(models.Model):
    name = models.TextField(max_length=25)
    def __str__(self) -> str:
        return self.name