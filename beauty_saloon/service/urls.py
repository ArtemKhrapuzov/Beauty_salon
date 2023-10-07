from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    path('models/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('models/register/', RegisterUser.as_view(), name='register'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/override_password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/override_password_reset_done.html'),
         name='password_reset_done'),

    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/override_password_reset_complete.html'),
         name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/override_password_reset_confirm.html', ),
         name='password_reset_confirm', ),
]
