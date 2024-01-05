from django.urls import path
from imagazine.users.views import *
from django.views.generic.base import TemplateView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('logout/', logout_user, name='logout'),
    path('activate/<str:uid64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('activate/email-confirmation-sent/', TemplateView.as_view(template_name='users/email_confirmation_sent.html'), name='email_confirmation_sent')
]