from django.db import models


CATEGORY = (
    ('гель-лаки', 'гель-лаки/база'),
    ('гель-лаки', 'гель-лаки/топ'),
    ('гель-лаки', 'гель-лаки/цветной гель-лак'),
    ('Наращивание и моделирование', 'Наращивание и моделирование/Гелевая система'),
    ('Наращивание и моделирование', 'Наращивание и моделирование/Полигель/акригель'),
    ('Наращивание и моделирование', 'Наращивание и моделирование/Акриловая система'),
    ('Наращивание и моделирование', 'Наращивание и моделирование/Формы и типсы'),
    ('Наращивание и моделирование', 'Наращивание и моделирование/Сопутствующие материалы'),
    ('Dip система/Дизайн ногтей', 'Dip система/Дизайн ногтей/Блестки'),
    ('Dip система/Дизайн ногтей', 'Dip система/Дизайн ногтей/Стемпинг дизайн'),
    ('Dip система/Дизайн ногтей', 'Dip система/Дизайн ногтей/Втирка'),
    ('Dip система/Дизайн ногтей', 'Dip система/Дизайн ногтей/Гель краска'),
    ('Dip система/Дизайн ногтей', 'Dip система/Дизайн ногтей/Кисти дизайна'),
    ('Уход за руками', 'Уход за руками/Масло для кутикулы'),
    ('Уход за руками', 'Уход за руками/Крем для рук'),
    ('Уход за руками', 'Уход за руками/Парафинотерапия'),
    ('Уход за руками', 'Уход за руками/Воск для кутикулы'),
    ('Уход за руками', 'Уход за руками/Средство для удаления кутикулы'),
    ('Уход за ногами', 'Уход за ногами/Крем для ног'),
    ('Уход за ногами', 'Уход за ногами/Дезодорирующие средства'),
    ('Уход за ногами', 'Уход за ногами/Педикюрные ванны'),
    ('Уход за ногами', 'Уход за ногами/Масло для ногтей'),
    ('Уход за ногами', 'Уход за ногами/Спец. средства'),
    ('Инструменты', 'Инструменты/Пилки основы и файлы для них'),
    ('Инструменты', 'Инструменты/Ножницы'),
    ('Инструменты', 'Инструменты/Щипцы и кусачки'),
    ('Инструменты', 'Инструменты/Пушеры'),
    ('Инструменты', 'Инструменты/Тампонодержатель (кюретки)'),
    ('Инструменты', 'Инструменты/Диски и файлы сменные'),
    ('Прочее', 'Прочее'),
)


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
    url = models.SlugField(max_length=160,  verbose_name='URL')
    cat = models.CharField(max_length=100, choices=CATEGORY)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'



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
