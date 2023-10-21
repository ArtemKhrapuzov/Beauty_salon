from django.urls import path

from service.views import *

urlpatterns = [
    path('', index, name='home'),
    #path('<slug:slug>/', ProductList.as_view(), name='product_detail'),
    path('category/<int:category_id>/<int:subtitle_id>/<int:subsub_id>/', ProductList.as_view(), name='product_list_by_subsub'),
]
