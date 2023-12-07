from django.db import models
from django.db.models import Avg
from django.urls import reverse

FOR_WHAT = (
    ('Для рук', 'Для рук'),
    ('Для ног', 'Для ног'),
    ('Для ногтей', 'Для ногтей'),
)

FOR_WHAT_TOOLS = (
    ('Для маникюра', 'Для маникюра'),
    ('Для педикюра', 'Для педикюра'),
)


class Trademark(models.Model):
    """Бренды"""
    title = models.CharField(max_length=70, verbose_name="Название бренда")
    url = models.SlugField(max_length=160, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name="Описание бренда")

    def get_absolute_url(self):
        return reverse('trademark_detail', kwargs={'slug': self.url})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['title']


class Product(models.Model):
    """Продукты"""
    name = models.CharField(max_length=255, verbose_name='Название')
    url = models.SlugField(max_length=160, unique=True, verbose_name='URL')
    trademark = models.ForeignKey(Trademark, verbose_name='Бренд', on_delete=models.CASCADE)
    compound = models.TextField(max_length=1000, verbose_name='Состав', blank=True, default='')
    volume = models.IntegerField(verbose_name='Объем (мл,гр)', blank=True, null=True)
    description = models.TextField(max_length=4000, blank=True, default='', verbose_name='Описание')
    color = models.CharField(max_length=50, verbose_name='Цвет', blank=True, default='')
    country = models.CharField(max_length=50, verbose_name='Страна производитель', blank=True, default='')
    density = models.CharField(max_length=50, verbose_name='Плотность', blank=True, default='')
    effect = models.CharField(max_length=50, verbose_name='Эффект', blank=True, default='')
    consistency = models.CharField(max_length=50, verbose_name='Консистенция', blank=True, default='')
    rigidity = models.CharField(max_length=50, verbose_name='Жесткость', blank=True, default='')
    shade = models.CharField(max_length=50, verbose_name='Оттенок', blank=True, default='')
    collection = models.CharField(max_length=50, verbose_name='Коллекция', blank=True, default='')
    for_what = models.CharField(max_length=30, verbose_name='Для чего', choices=FOR_WHAT, blank=True, default='')
    for_what_tools = models.CharField(max_length=30, verbose_name='Для чего инструменты', choices=FOR_WHAT_TOOLS,
                                      blank=True, default='')
    best_before_date = models.CharField(max_length=50, verbose_name='Срок годность', blank=True, default='')
    where_buy = models.CharField(max_length=50, verbose_name='Где купить', blank=True, default='')
    link = models.TextField(max_length=2000, verbose_name='Ссылка на товар', blank=True, default='')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name='Фото')
    cat = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    subtitle = models.ForeignKey('Subtitle', verbose_name='Подкатегория', on_delete=models.CASCADE, blank=True,
                                 default='')
    subsub = models.ForeignKey('Subsubtitle', verbose_name='Подподкатегория', on_delete=models.CASCADE, blank=True,
                               default='')

    def save(self, *args, **kwargs):
        self.color = self.color.lower()
        self.density = self.density.lower()
        self.effect = self.effect.lower()
        self.consistency = self.consistency.lower()
        self.rigidity = self.rigidity.lower()
        self.shade = self.shade.lower()
        super().save(*args, **kwargs)

    def average_rating(self):
        result = Rating.objects.filter(product=self).aggregate(Avg('star'))['star__avg']
        return str(round(result, 1)).replace(',', '.')

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.url})

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-id']


class Category(models.Model):
    """Категории"""
    title = models.CharField(max_length=50, verbose_name='Название категории')
    url = models.SlugField(max_length=160, verbose_name='URL')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subtitle(models.Model):
    """Подкатегории"""
    title = models.CharField(max_length=50, verbose_name='Название подкатегории')
    url = models.SlugField(max_length=160, verbose_name='URL')
    cat = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cat} / {self.title}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Subsubtitle(models.Model):
    """Подподкатегории"""
    title = models.CharField(max_length=50, verbose_name='Подподкатегория')
    url = models.SlugField(max_length=160, verbose_name='URL')
    sub = models.ForeignKey('Subtitle', verbose_name='Подкатегория', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sub} / {self.title}'

    class Meta:
        verbose_name = 'Подподкатегория'
        verbose_name_plural = 'Подподкатегории'


class Reviews(models.Model):
    """Отзывы продуктов"""
    email = models.EmailField(verbose_name='Mail')
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey('RatingStar', on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="продукт")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ["-value"]


class Article(models.Model):
    """Статьи"""
    title = models.CharField(max_length=100, verbose_name='Заголовок', unique=True)
    url = models.SlugField(max_length=160, unique=True, verbose_name='URL')
    image = models.ImageField(upload_to="article/%Y/%m/%d/", verbose_name='Фото')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    description_1 = models.TextField(max_length=4000, blank=True, default='', verbose_name='Текст_1')
    image_1 = models.ImageField(upload_to="article/%Y/%m/%d/", blank=True, null=True, verbose_name='Фото_1')
    description_2 = models.TextField(max_length=4000, blank=True, default='', verbose_name='Текст_2')
    image_2 = models.ImageField(upload_to="article/%Y/%m/%d/", blank=True, null=True, verbose_name='Фото_2')
    description_3 = models.TextField(max_length=4000, blank=True, default='', verbose_name='Текст_3')
    image_3 = models.ImageField(upload_to="article/%Y/%m/%d/", blank=True, null=True, verbose_name='Фото_3')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.articlereview_set.filter(parent__isnull=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-id']


class ArticleReview(models.Model):
    """Отзывы статей"""
    email = models.EmailField(verbose_name='Mail')
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    article = models.ForeignKey(Article, verbose_name="Продукт", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.article}'

    class Meta:
        verbose_name = 'Отзыв статьи'
        verbose_name_plural = 'Отзывы статей'
