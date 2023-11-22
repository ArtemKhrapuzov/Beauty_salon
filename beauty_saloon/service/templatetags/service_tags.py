from django import template
from django.db.models import Prefetch, Count, OuterRef, Subquery

from service.models import *
from django.core.cache import cache


register = template.Library()


@register.simple_tag()
def get_category():
    return Category.objects.all()

@register.simple_tag
def get_subtitle(category_id):
    return Subtitle.objects.filter(cat=category_id)


# @register.simple_tag
# def get_subtitle(category_id):
#     cache_key = f"subtitle_{category_id}"
#     subtitles = cache.get(cache_key)
#
#     if subtitles is None:
#         subtitles = Subtitle.objects.filter(cat=category_id)
#         cache.set(cache_key, subtitles)
#
#     return subtitles


@register.simple_tag
def get_subsubtitle(subtitle_id):
    return Subsubtitle.objects.filter(sub=subtitle_id)

# @register.simple_tag
# def get_subsubtitle(subtitle_id):
#     cache_key = f"subtitle_{subtitle_id}"
#     subtitles = cache.get(cache_key)
#
#     if subtitles is None:
#         subtitles = Subsubtitle.objects.filter(sub=subtitle_id).prefetch_related('sub')
#         cache.set(cache_key, subtitles)
#
#     return subtitles

@register.simple_tag
def get_trademark():
    return Trademark.objects.all().values('id', 'title', 'url')


# @register.simple_tag
# def get_trademark():
#     return Trademark.objects.all().annotate(
#         name=Subquery(Product.objects.filter(trademark_id=OuterRef('id')).values('trademark__title')[:1]))
