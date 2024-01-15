from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:id>/', AddProductCartView.as_view(), name='add'),
    path('remove/<int:id>/', RemoveProductCart.as_view(), name='remove'),
    path('', IndexCart.as_view(), name='index')
]