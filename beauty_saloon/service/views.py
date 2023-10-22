from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from service.models import *



def index(request):
    return render(request, 'service/index.html')


class ProductList(ListView):
    model = Product
    slug_field = 'url'
    context_object_name = 'products'


    def get_queryset(self):
        """Переход по меню"""
        subsub_slug = self.kwargs['subsub_slug']
        subsubtitle = get_object_or_404(Subsubtitle, url=subsub_slug)
        queryset = super().get_queryset()
        return queryset.filter(subsub=subsubtitle)


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    slug_field = 'url'



