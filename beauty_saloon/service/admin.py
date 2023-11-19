from django.contrib import admin

from service.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "trademark", "cat", "subtitle")
    list_filter = ("cat", "subtitle", "name", "trademark")
    search_fields = ("name", "trademark")
    ordering = ('-id',)
    prepopulated_fields = {"url": ("name", "trademark", "cat")}


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("title",)
#     list_filter = ("title",)
#     search_fields = ("title",)
#
#     prepopulated_fields = {"url": ("title",)}


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "product", "id")
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "product", "ip")


@admin.register(Subsubtitle)
class SubsubtitleAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)

    prepopulated_fields = {"url": ("title",)}


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("title",)
    search_fields = ("title",)

    prepopulated_fields = {"url": ("title",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)
    list_filter = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"url": ("title",)}

@admin.register(ArticleReview)
class ArticleReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "article", "id")
    readonly_fields = ("name", "email")

@admin.register(Trademark)
class TrademarkAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"url": ("title",)}


# admin.site.register(RatingStar)
