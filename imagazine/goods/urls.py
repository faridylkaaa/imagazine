from django.urls import path, include
from imagazine.goods.views import *

urlpatterns = [ 
               path('', IndexView.as_view(), name='main'),
               path('games/', GamesIndexView.as_view(), name='index'),
               path('console/', ConsolesView.as_view(), name='consoles_index'),
               path('console/<int:pk>/', ConsoleView.as_view(), name='console'),
               path('games/<int:pk>/', ProfileGameView.as_view(), name='profile'),
               path('love/<int:pk>/', LoveIndexView.as_view(), name='loves'), 
               path('love/remove/<int:pk>/<int:id>/', RemoveLoveView.as_view(), name='remove_love'),
               path('love/add/<int:pk>/<int:id>/', LoveAddView.as_view(), name='add_love')
               ]