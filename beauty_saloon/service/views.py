import random
from django.db.models import Count, Subquery, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.postgres.search import SearchVector

from .forms import ReviewForm, RatingForm, ArticleReviewForm
from .models import *
from .utils import QuerysetMixin


class Index(ListView):
    """ВАЖНО! Корректно работает, только после введеных трех и более продуктов в БД.
    Не ввел if с целью оптимизации запроса. Отображение товаров со средним рейтингом выше 4.0,
    новинок (рандомно 3 из последних 12), статей (последние 3)"""
    model = Product
    template_name = 'service/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Запрос в бд на продукты с средним рейтингом 4+,
        оптимизированный запрос с выводом колличества комментариев"""
        queryset = Product.objects.select_related('trademark').select_related('cat') \
                       .annotate(avg_rating=Avg('rating__star__value')) \
                       .annotate(num_reviews=Subquery(
            Reviews.objects.filter(product_id=OuterRef('id'))
            .values('product_id')
            .annotate(count=Count('id'))
            .values('count')[:1]
        )) \
                       .filter(avg_rating__gte=4) \
                       .only('id', 'name', 'url', 'trademark__title', 'cat__title', 'image') \
                       .order_by('?')[:3]
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Вывод новинок и статей"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Интернет портал косметики'
        queryset_new = Product.objects.select_related('trademark').select_related('cat').order_by('-id')[:12].only(
            'id', 'name', 'url', 'trademark__title', 'cat__title', 'image').annotate(
            avg_rating=Avg('rating__star__value'))
        context['products_new'] = random.sample(list(queryset_new), 3)

        queryset_article = Article.objects.filter(is_published=True)[:3].only(
            'title', 'description_1', 'image', 'url', 'id')
        context['articles'] = queryset_article

        return context


class ArticleList(ListView):
    """ВАЖНО работает корректно при добавлении 6 и более продуктов в БД.
        Все статьи"""
    model = Article
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.all().only('url', 'title', 'description_1', 'image') \
            .annotate(num_reviews_art=Subquery(
            ArticleReview.objects.filter(article_id=OuterRef('id'))
            .values('article_id')
            .annotate(count=Count('id'))
            .values('count')[:1]))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Статьи'

        queryset_new = Product.objects.select_related('trademark').select_related('cat') \
                           .select_related('subsub').only(
            'id', 'name', 'url', 'trademark__title', 'color', 'cat__title', 'image', 'subsub__title') \
                           .order_by('-id')[:12].annotate(
            avg_rating=Avg('rating__star__value')).annotate(num_reviews=Subquery(
            Reviews.objects.filter(product_id=OuterRef('id'))
            .values('product_id')
            .annotate(count=Count('id'))
            .values('count')[:1]
        ))
        random_products_new = random.sample(list(queryset_new), 5)
        context['products_new'] = random_products_new
        return context


class ArticleDetail(DetailView):
    """ВАЖНО работает корректно при добавлении 6 и более продуктов в БД.
        Детальный обзор статьи"""
    model = Article
    context_object_name = 'article'
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title}'

        queryset_new = Product.objects.select_related('trademark').select_related('cat') \
                           .select_related('subsub').only(
            'id', 'name', 'url', 'trademark__title', 'color', 'cat__title', 'image', 'subsub__title') \
                           .order_by('-id')[:18].annotate(
            avg_rating=Avg('rating__star__value')).annotate(num_reviews=Subquery(
            Reviews.objects.filter(product_id=OuterRef('id'))
            .values('product_id')
            .annotate(count=Count('id'))
            .values('count')[:1]
        ))
        random_products_new = random.sample(list(queryset_new), 6)
        context['products_new'] = random_products_new

        context["star_form"] = RatingForm

        article_reviews = self.object.get_review().prefetch_related('articlereview_set')
        context['article_reviews'] = article_reviews

        return context


class TrademarkDetail(DetailView):
    """Отображение всех брендов"""
    model = Trademark
    context_object_name = 'trademark'
    slug_field = 'url'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Передача queryset с продуктами данного бренда"""
        context = super().get_context_data(**kwargs)
        products = Product.objects.select_related('trademark').select_related('cat').select_related('subsub').only(
            'id', 'name', 'url', 'trademark__title', 'color', 'cat__title', 'image', 'subsub__title') \
            .filter(trademark__url=self.kwargs.get('slug')).annotate(
            avg_rating=Avg('rating__star__value')).annotate(num_reviews=Subquery(
            Reviews.objects.filter(product_id=OuterRef('id'))
            .values('product_id')
            .annotate(count=Count('id'))
            .values('count')[:1]))
        context['products'] = products
        context['title'] = f'{self.object.title}'
        return context


class ProductList(QuerysetMixin, ListView):
    """queryset отфильтрованных продуктов по заданным категориям/подкатегориям/подподкатегориям."""

    def get_queryset(self):
        subsub_slug = self.kwargs.get('subsub_slug')
        if subsub_slug:
            subsubtitle = get_object_or_404(Subsubtitle.objects.only('url'), url=subsub_slug)
        else:
            subsubtitle = None
        subtitle_slug = self.kwargs['subtitle_slug']
        subtitle = get_object_or_404(Subtitle.objects.only('url'), url=subtitle_slug)
        queryset = super().get_queryset()
        if subsubtitle:
            queryset = queryset.filter(subsub=subsubtitle)
        return queryset.select_related('trademark').select_related('cat').select_related('subsub').filter(
            subtitle=subtitle) \
            .annotate(num_reviews=Subquery(Reviews.objects.filter(product_id=OuterRef('id'))
                                           .values('product_id')
                                           .annotate(count=Count('id'))
                                           .values('count')[:1])).only(
            'id', 'name', 'url', 'color', 'trademark__title', 'cat__title', 'subsub__title', 'image') \
            .annotate(avg_rating=Avg('rating__star__value'))

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
    """Прочее"""

    def get_queryset(self):
        cat_slug = self.kwargs.get('cat_slug')
        if cat_slug:
            cattitle = get_object_or_404(Category.objects.only('url'), url=cat_slug)
        else:
            cattitle = None
        queryset = super().get_queryset()
        if cattitle:
            queryset = queryset.filter(cat=cattitle)
        return queryset.select_related('trademark').select_related('cat').annotate(
            avg_rating=Avg('rating__star__value')).only(
            'id', 'name', 'url', 'color', 'trademark', 'cat__title', 'subsub__title', 'image')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(url=self.kwargs['cat_slug'])
        category_title = category.title
        context['category_title'] = category_title
        context['title'] = 'Прочее'
        return context


class Filter(QuerysetMixin, ListView):
    """Сортировка"""
    template_name = 'service/filter_result.html'

    def get_queryset(self):
        """Сортировка по категории и полю"""
        queryset = Product.objects.filter(cat__url=self.kwargs['cat_url']).annotate(
            avg_rating=Avg('rating__star__value'))
        fields = ['trademark__title', 'color', 'volume', 'for_what', 'for_what_tools']
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

    def get_queryset(self):
        return super().get_queryset().select_related('subtitle').select_related('cat').select_related('trademark')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm
        context['title'] = f'{self.object.name}, {self.object.trademark}'

        product_reviews = self.object.get_review().prefetch_related('reviews_set')
        context['product_reviews'] = product_reviews
        return context


class NewProduct(ListView):
    """Новинки. Вывод последних n записей из БД Product """
    model = Product
    template_name = 'service/new.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        return Product.objects.select_related('trademark').select_related('cat').select_related('subsub') \
                   .annotate(avg_rating=Avg('rating__star__value')) \
                   .annotate(num_reviews=Subquery(Reviews.objects.filter(product_id=OuterRef('id'))
                                                  .values('product_id')
                                                  .annotate(count=Count('id'))
                                                  .values('count')[:1])).only(
            'id', 'name', 'url', 'color', 'trademark__title', 'cat__title', 'subsub__title', 'image').order_by('-id')[
               :200]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новинки'

        return context


class HitProduct(ListView):
    """Хиты. Вывод товаров с рейтингом 4 и выше на отдельном url"""
    model = Product
    template_name = 'service/hit.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.select_related('trademark').select_related('cat').select_related('subsub') \
            .annotate(avg_rating=Avg('rating__star__value')).filter(avg_rating__gte=4) \
            .annotate(num_reviews=Subquery(Reviews.objects.filter(product_id=OuterRef('id'))
                                           .values('product_id')
                                           .annotate(count=Count('id'))
                                           .values('count')[:1])).only(
            'id', 'name', 'url', 'color', 'trademark__title', 'cat__title', 'subsub__title', 'image')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Хиты'
        return context


class AddReview(View):
    """Отзывы продуктов"""

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


class AddReviewArticle(View):
    """Отзывы статей"""

    def post(self, request, pk):
        form = ArticleReviewForm(request.POST)
        article = Article.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.article = article
            form.save()
        return redirect(article.get_absolute_url())


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
    paginate_by = 9

    def get_queryset(self):
        search_vector = SearchVector('name', 'trademark__title', 'color')
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            return Product.objects.select_related('trademark').select_related('cat').select_related('subsub') \
                .annotate(search=search_vector).filter(search=query_string) \
                .annotate(avg_rating=Avg('rating__star__value')) \
                .annotate(num_reviews=Subquery(Reviews.objects.filter(product_id=OuterRef('id')).values('product_id')
                                               .annotate(count=Count('id'))
                                               .values('count')[:1])).only(
                'id', 'name', 'url', 'color', 'trademark__title', 'cat__title', 'subsub__title', 'image')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def about(request):
    """О сайте"""
    return render(request, 'service/about.html')
