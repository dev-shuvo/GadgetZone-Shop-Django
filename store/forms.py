from django import forms

from store.models import ProductReview


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ["review", "rating"]
