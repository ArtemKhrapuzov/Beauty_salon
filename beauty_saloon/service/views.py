from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from service.models import *


class CatTrademarkCountryColor:
    """queryset для фильтров"""

    def get_trademarks(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('trademark').values_list('trademark',
                                                                                               flat=True).distinct()
        else:
            return []

    def get_colors(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('color').values_list('color',
                                                                                           flat=True).distinct()
        else:
            return []

    def get_volumes(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('volume').values_list('volume',
                                                                                            flat=True).distinct()
        else:
            return []

    def get_for_whats(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('for_what').values_list('for_what',
                                                                                              flat=True).distinct()
        else:
            return []

    def get_for_what_tools(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('for_what_tools').\
                values_list('for_what_tools', flat=True).distinct()
        else:
            return []


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


class ProductOtherList(CatTrademarkCountryColor, ListView):
    """ context and queryset for Прочее"""
    model = Product
    slug_field = 'url'
    context_object_name = 'products'

    def get_queryset(self):
        cat_slug = self.kwargs.get('cat_slug')
        if cat_slug:
            cattitle = get_object_or_404(Category, url=cat_slug)
        else:
            cattitle = None
        queryset = super().get_queryset()
        if cattitle:
            queryset = queryset.filter(cat=cattitle)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_count = self.get_queryset().count()

        category = Category.objects.get(url=self.kwargs['cat_slug'])
        category_title = category.title

        context['products_count'] = products_count
        context['category_title'] = category_title
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
        if "volume" in self.request.GET:
            queryset = queryset.filter(volume__in=self.request.GET.getlist("volume"))
        if "for_what" in self.request.GET:
            queryset = queryset.filter(for_what__in=self.request.GET.getlist("for_what"))
        if "for_what_tools" in self.request.GET:
            queryset = queryset.filter(for_what_tools__in=self.request.GET.getlist("for_what_tools"))
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
