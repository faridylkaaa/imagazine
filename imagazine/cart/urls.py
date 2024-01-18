from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:id>/', AddProductCartView.as_view(), name='add'),
    path('remove/<int:id>/', RemoveProductCart.as_view(), name='remove'),
    path('', IndexCart.as_view(), name='index'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/api/', YoomoneyNotifView.as_view(), name='notif')
]