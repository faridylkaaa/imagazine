from django.urls import path
from imagazine.users.views import *

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('logout/', logout_user, name='logout')
]