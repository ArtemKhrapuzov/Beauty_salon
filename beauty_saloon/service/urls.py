from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
]
