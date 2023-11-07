from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector

from .forms import ReviewForm, RatingForm
from .models import *
from .utils import QuerysetMixin


class Index(ListView):
    """Главная"""
    model = Product
    template_name = 'service/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Интернет портал косметики'
        return context


class ProductList(QuerysetMixin, ListView):
    """Product list"""

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
        context['category_title'] = category_title
        context['subtitle_title'] = subtitle_title
        context['title'] = f'{category_title}, {subtitle_title}'
        return context


class ProductOtherList(QuerysetMixin, ListView):
    """ context and queryset for Прочее"""

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
        category = Category.objects.get(url=self.kwargs['cat_slug'])
        category_title = category.title
        context['category_title'] = category_title
        context['title'] = f'{category_title}'
        return context


class Filter(QuerysetMixin, ListView):
    """Сортировка"""
    template_name = 'service/filter_result.html'

    def get_queryset(self):
        """Сортировка по категории и полю"""
        queryset = Product.objects.filter(cat__url=self.kwargs['cat_url'])
        fields = ['trademark', 'color', 'volume', 'for_what', 'for_what_tools']
        for field in fields:
            if field in self.request.GET:
                queryset = queryset.filter(**{f'{field}__in': self.request.GET.getlist(field)})
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сортировка товаров'
        return context


class ProductDetail(DetailView):
    """Show product"""
    model = Product
    context_object_name = 'product'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm
        context['title'] = f'{self.object.name}, {self.object.trademark}'
        return context


class NewProduct(ListView):
    """Новинки. Вывод последних n записей из БД Product """
    model = Product
    template_name = 'service/new.html'
    context_object_name = 'products'
    paginate_by = 60

    def get_queryset(self):
        return Product.objects.all().order_by('-id')[:200]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новинки'
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return redirect(product.get_absolute_url())


class AddStarRating(View):
    """Добавление рейтинга продукту"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                product_id=int(request.POST.get('product')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск продуктов"""
    template_name = 'service/filter_result.html'
    context_object_name = 'products'
    paginate_by = 60

    def get_queryset(self):
        search_vector = SearchVector('name', 'trademark', 'color')
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            return Product.objects.annotate(search=search_vector).filter(search=query_string)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
