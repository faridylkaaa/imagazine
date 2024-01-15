from django.db import models

# Create your models here.
class Product(models.Model):
    product = models.CharField(max_length=10, blank=True, null=True)
    
    
from django.db import models
from imagazine.labels.models import *

class ProductN(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=250)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='images/goods/console/')
    
    def get_model(self):
        try:
            return self.auto
        except:
            return self.bus

# Create your models here.
class Auto(ProductN):
    category = models.ManyToManyField(CategoryGame)
    compatibility = models.ForeignKey(ModelConsole, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
class Bus(ProductN):
    model_console = models.ForeignKey(ModelConsole, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name