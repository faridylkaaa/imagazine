from django.db import models
from imagazine.labels.models import *

class Goods(models.Model):
    name = models.TextField(max_length=250)
    description = models.TextField(max_length=500)
    model_console = models.ForeignKey(ModelConsole, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    def get_model(self):
        try:
            return self.game
        except:
            return self.console

    
# Create your models here.
class Game(Goods):
    category = models.ManyToManyField(CategoryGame)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name
    
    def is_game(self):
        return True
    
class Console(Goods):
    pass
    
    def __str__(self) -> str:
        return self.name
    
    def is_game(self):
        return False

class Gallery(models.Model):
    image = models.ImageField(upload_to='images/goods/console/') # вот тут бы ссылку поменять
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, related_name='photos')