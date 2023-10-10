from django.contrib import admin

from service.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "trademark", "category")
    list_filter = ("category", "name", "trademark")
    search_fields = ("name", "trademark")

    prepopulated_fields = {"url": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    list_filter = ("title", "subtitle")
    search_fields = ("title", "subtitle")

    prepopulated_fields = {"url": ("title",)}


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "product", "id")
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "ip")


admin.site.register(RatingStar)
admin.site.register(Subtitle)