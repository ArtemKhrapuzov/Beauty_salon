from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from django.views.generic import TemplateView

from users.views import *

urlpatterns = [

   # path('login/', MyLoginView.as_view(), name='login'),
    path('models/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('agree/', agree, name='agree'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'),
         name='confirm_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='registration/invalid_verify.html'),
         name='invalid_verify'
         ),

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
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(),
         name='verify_email')
]
