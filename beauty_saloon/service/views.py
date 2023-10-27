from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from service.models import *


class CatTrademarkCountryColor:
    """Кверисет для фильтров по категориям, бренду, стране и цвету"""

    def get_trademarks(self):
        return Product.objects.all().values('trademark').distinct()

    def get_colors(self):
        return Product.objects.all().values('color').distinct()

    def get_countrys(self):
        return Product.objects.all().values('country').distinct()

    def get_cats(self):
        return Product.objects.all().values('subsub__title').distinct()


class Index(ListView):
    """Главная"""
    model = Product
    template_name = 'service/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()


class ProductList(CatTrademarkCountryColor, ListView):
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
        return context


class Filter(CatTrademarkCountryColor, ListView):
    """Фильтр"""
    template_name = 'service/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        if "trademark" in self.request.GET:
            queryset = queryset.filter(trademark__in=self.request.GET.getlist("trademark"))
        if "color" in self.request.GET:
            queryset = queryset.filter(color__in=self.request.GET.getlist("color"))
        if "category" in self.request.GET:
            queryset = queryset.filter(subsub__title__in=self.request.GET.getlist("category"))
        return queryset


class ProductDetail(DetailView):
    """Show product"""
    model = Product
    context_object_name = 'product'
    slug_field = 'url'


class NewProduct(ListView):
    """Новинки. Вывод последних 10 записей из БД Product """
    model = Product
    template_name = 'service/new.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('-id')[:10]
