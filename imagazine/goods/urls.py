from django.urls import path, include
from imagazine.goods.views import *

urlpatterns = [ 
               path('', IndexView.as_view(), name='index')]