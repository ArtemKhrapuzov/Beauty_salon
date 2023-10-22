from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    path('new_items/', NewProduct.as_view(), name='new_items'),
    path('catalog/<slug:subsub_slug>/', ProductList.as_view(), name='product_list_by_subsub'),
    path('cat/<str:slug>/', ProductDetail.as_view(), name='product_detail'),

]
