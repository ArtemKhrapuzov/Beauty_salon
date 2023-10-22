from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    path('catalog/<slug:subsub_slug>/', ProductList.as_view(), name='product_list_by_subsub'),
    path('<str:slug>/', ProductDetail.as_view(), name='product_detail')
]
