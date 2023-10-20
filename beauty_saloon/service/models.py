from django.db import models


class Product(models.Model):
    """Продукты"""
    name = models.CharField(max_length=255, verbose_name='Название')
    trademark = models.CharField(max_length=255, unique=True, verbose_name='Название торговой марки')
    compound = models.TextField(max_length=1000, verbose_name='Состав')
    volume = models.CharField(max_length=30, verbose_name='Объем')
    description = models.TextField(max_length=4000, blank=True, default='', verbose_name='Описание')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    country = models.CharField(max_length=50, verbose_name='Страна производитель')
    best_before_date = models.CharField(max_length=50, verbose_name='Срок годность')
    where_buy = models.CharField(max_length=50, verbose_name='Где купить')
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Фото')
    cat = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)
    subtitle = models.ForeignKey('Subtitle', verbose_name='Подкатегория', on_delete=models.CASCADE, null=True,
                                 blank=True)
    subsub = models.ForeignKey('Subsubtitle', verbose_name='Подподкатегория', on_delete=models.CASCADE, null=True,
                                 blank=True)
    url = models.SlugField(max_length=160, verbose_name='URL')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    url = models.SlugField(max_length=160, verbose_name='URL')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Subtitle(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название подкатегории')
    cat = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cat} / {self.title}'

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Subsubtitle(models.Model):
    title = models.CharField(max_length=50, verbose_name='Подподкатегория')
    sub = models.ForeignKey('Subtitle', verbose_name='Подкатегория', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.sub} / {self.title}'

    class Meta:
        verbose_name = 'Подподкатегория'
        verbose_name_plural = 'Подподкатегории'

class Reviews(models.Model):
    """Отзывы"""
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
