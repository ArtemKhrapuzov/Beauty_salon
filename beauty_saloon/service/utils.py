from .models import Product


class QuerysetMixin:
    """queryset для фильтров"""
    model = Product
    context_object_name = 'products'
    paginate_by = 3

    def get_trademarks(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('trademark__title')\
                .values_list('trademark__title', flat=True).distinct()
        else:
            return []

    def get_colors(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('color').values_list('color',
                                                                                           flat=True).distinct()
        else:
            return []

    def get_volumes(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('volume').values_list('volume',
                                                                                            flat=True).distinct()
        else:
            return []

    def get_for_whats(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('for_what').values_list('for_what',
                                                                                              flat=True).distinct()
        else:
            return []

    def get_for_what_tools(self):
        if 'cat_slug' in self.kwargs:
            cat_slug = self.kwargs['cat_slug']
            return Product.objects.filter(cat__url=cat_slug).order_by('for_what_tools'). \
                values_list('for_what_tools', flat=True).distinct()
        else:
            return []
