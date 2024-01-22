from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:id>/', AddProductCartView.as_view(), name='add'),
    path('remove/<int:id>/', RemoveProductCart.as_view(), name='remove'),
    path('', IndexCart.as_view(), name='index'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/api/', YoomoneyNotifView.as_view(), name='notif'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order')
]