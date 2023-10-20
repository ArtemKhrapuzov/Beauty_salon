from django import template

from service.models import *


register = template.Library()


@register.simple_tag()
def get_category():
    return Category.objects.all()

@register.simple_tag
def get_subtitle(category_id):
    return Subtitle.objects.filter(cat=category_id)


@register.simple_tag
def get_subsubtitle(subtitle_id):
    return Subsubtitle.objects.filter(sub=subtitle_id)
