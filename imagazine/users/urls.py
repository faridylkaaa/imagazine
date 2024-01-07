from django.urls import path
from imagazine.users.views import *
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('logout/', logout_user, name='logout'),
    path('activate/<str:uid64>/<str:token>/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('activate/email-confirmation-sent/', TemplateView.as_view(template_name='users/email_confirmation_sent.html'), name='email_confirmation_sent'),
    path('activate/email-not-confirm/', TemplateView.as_view(template_name='users/email_not_confirm.html'), name='email_not_confirm'),
    path('<int:pk>/', ProfileUserView.as_view(), name='profile_user'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html', email_template_name='users/password_reset_email.html', success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='delete')
]