from django import forms
from django.contrib.auth import get_user_model

from .models import Reviews, RatingStar, Rating, ArticleReview

User = get_user_model()


class ReviewForm(forms.ModelForm):
    """Форма отзыва продукта"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class ArticleReviewForm(forms.ModelForm):
    """Форма отзыва статей"""
    class Meta:
        model = ArticleReview
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star", )
