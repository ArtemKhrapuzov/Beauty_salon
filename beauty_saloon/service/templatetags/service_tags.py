from django import template

from service.models import *
from django.core.cache import cache

register = template.Library()


@register.simple_tag
def get_category():
    """Кэширование категорий в меню на 360сек"""
    cache_key = 'category_id'
    category = cache.get(cache_key)

    if category is None:
        category = Category.objects.all()
        cache.set(cache_key, category, timeout=360)
    return category


@register.simple_tag
def get_subtitle(category_id):
    """Кэширование подзаголовков на 360сек"""
    cache_key = f"subtitle_{category_id}"
    subtitles = cache.get(cache_key)

    if subtitles is None:
        subtitles = Subtitle.objects.filter(cat=category_id)
        cache.set(cache_key, subtitles, timeout=360)

    return subtitles


@register.simple_tag
def get_subsubtitle(subtitle_id):
    """Кэширование подподзаголовков на 360сек"""
    cache_key = f"subsubtitle_{subtitle_id}"
    subtitles = cache.get(cache_key)

    if subtitles is None:
        subtitles = Subsubtitle.objects.filter(sub=subtitle_id).prefetch_related('sub')
        cache.set(cache_key, subtitles, timeout=360)

    return subtitles


@register.simple_tag
def get_trademark():
    """Кэширование брендов в меню на 360сек"""
    cache_key = 'trademark_id'
    trademark = cache.get(cache_key)

    if trademark is None:
        trademark = Trademark.objects.all().only('title', 'url')
        cache.set(cache_key, trademark, timeout=360)
    return trademark
