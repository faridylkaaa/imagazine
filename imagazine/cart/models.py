from django.db import models
from imagazine.users.models import User
from imagazine.goods.models import Goods

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name='orders')
    payment = models.CharField(max_length=50, blank=True, null=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name='items')
    product = models.ForeignKey(Goods, on_delete = models.CASCADE)
    count = models.PositiveIntegerField()