from django.urls import path, include
from imagazine.goods.views import *

urlpatterns = [ 
               path('', IndexView.as_view(), name='main'),
               path('games/', GamesIndexView.as_view(), name='index'),
               path('console/', ConsolesView.as_view(), name='consoles_index'),
               path('console/<int:pk>/', ConsoleView.as_view(), name='console'),
               path('games/<int:pk>/', ProfileGameView.as_view(), name='profile')]