from django import forms
from django.contrib.auth import get_user_model

from .models import Reviews

User = get_user_model()


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")



