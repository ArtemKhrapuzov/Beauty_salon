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
        subsub_slug = self.kwargs.get('subsub_slug')
        if subsub_slug:
            subsubtitle = get_object_or_404(Subsubtitle, url=subsub_slug)
        else:
            subsubtitle = None
        subtitle_slug = self.kwargs['subtitle_slug']
        subtitle = get_object_or_404(Subtitle, url=subtitle_slug)
        queryset = super().get_queryset()
        if subsubtitle:
            queryset = queryset.filter(subsub=subsubtitle)
        return queryset.filter(subtitle=subtitle)



class ProductDetail(DetailView):
    """Show product"""
    model = Product
    context_object_name = 'product'
    slug_field = 'url'


class NewProduct(ListView):
    """Вывод последних 10 записей из БД Product"""
    model = Product
    template_name = 'service/new.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('-id')[:10]
