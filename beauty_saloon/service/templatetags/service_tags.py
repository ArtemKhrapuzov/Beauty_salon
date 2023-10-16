from django import template

from service.models import *


register = template.Library()


@register.simple_tag()
def get_category():
    return Category.objects.all()

@register.simple_tag()
def get_subtitle(cat_id):
    return Subtitle.objects.filter(cat_id=cat_id)
