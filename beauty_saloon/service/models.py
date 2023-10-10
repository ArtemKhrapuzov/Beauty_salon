from django.db import models


class Product(models.Model):
    """Продукты"""
    name = models.CharField(max_length=255)
    trademark = models.CharField(max_length=255, unique=True)
    compound = models.TextField(max_length=1000)
    volume = models.CharField(max_length=30)
    description = models.TextField(max_length=4000, blank=True, default='')
    color = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    best_before_date = models.CharField(max_length=50)
    where_buy = models.CharField(max_length=50)
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото')
    category = models.ForeignKey('Category', verbose_name="Категория", on_delete=models.PROTECT)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50, blank=True, default='')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return f'{self.title} - {self.subtitle}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="фильм")

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
        ordering = ["value"]
