from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register')
]