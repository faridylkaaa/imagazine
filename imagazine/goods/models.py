from django.db import models
from imagazine.labels.models import *

# Create your models here.
class Game(models.Model):
    name = models.TextField(max_length=25)
    description = models.TextField(max_length=75)
    category = models.ManyToManyField(CategoryGame)
    compatibility = models.ForeignKey(ModelConsole, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name
    
class Console(models.Model):
    name = models.TextField(max_length=25)
    description = models.TextField(max_length=75)
    model_console = models.ForeignKey(ModelConsole, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return self.name