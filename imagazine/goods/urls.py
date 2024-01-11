from django.urls import path, include
from imagazine.goods.views import *

urlpatterns = [ 
               path('', GamesIndexView.as_view(), name='index'),
               path('games/<int:pk>/', ProfileGameView.as_view(), name='profile')]