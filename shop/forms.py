from django import forms
from shop.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Your review'}))
    
    class Meta:
        model = ProductReview
        fields = ['review','rating']