from django.urls import path
from imagazine.users.views import *

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login')
]