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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subtitle_slug = self.kwargs['subtitle_slug']
        subtitle = get_object_or_404(Subtitle, url=subtitle_slug)
        category_title = subtitle.cat.title
        subtitle_title = subtitle.title
        products_count = self.get_queryset().count()
        context['category_title'] = category_title
        context['subtitle_title'] = subtitle_title
        context['products_count'] = products_count
        # добавляем список всех возможных позиций в выпадающее меню
        context['trademarks'] = Product.objects.values_list('trademark', flat=True).distinct()
        context['cat'] = Product.objects.values_list('subsub__title', flat=True).distinct()
        context['countrys'] = Product.objects.values_list('country', flat=True).distinct()
        context['colors'] = Product.objects.values_list('color', flat=True).distinct()
        return context


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
