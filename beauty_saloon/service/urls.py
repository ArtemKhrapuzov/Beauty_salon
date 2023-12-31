from django.urls import path

from service.views import *

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('about/', about, name='about'),
    path('search/', Search.as_view(), name='search'),
    path('new_items/', NewProduct.as_view(), name='new_items'),
    path('hit_items/', HitProduct.as_view(), name='hit_items'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('article/<str:slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('filter/<slug:cat_url>/', Filter.as_view(), name='filter'),
    path('catalog/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('review_article/<int:pk>/', AddReviewArticle.as_view(), name='add_review_article'),
    path('trademark/<slug:slug>/', TrademarkDetail.as_view(), name='trademark_detail'),
    path('<slug:cat_slug>/', ProductOtherList.as_view(), name='product_list_cat'),
    path('<slug:cat_slug>/<slug:subtitle_slug>/', ProductList.as_view(), name='product_list_sub'),
    path('<slug:cat_slug>/<slug:subtitle_slug>/<slug:subsub_slug>/', ProductList.as_view(), name='product_list_subsub'),
]
