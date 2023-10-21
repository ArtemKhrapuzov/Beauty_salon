from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    path('catalog/<int:subsub_id>/', ProductList.as_view(), name='product_list_by_subsub'),
]
