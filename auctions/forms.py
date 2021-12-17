from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets

from .models import *

class ListingForm(forms.ModelForm):
    title = forms.CharField(max_length=64, label="Title Item", widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(max_length=64, label="Description", widget=forms.TextInput(attrs={'class':'form-control'}))
    startingBid = forms.IntegerField(label="Starting Price",widget=forms.NumberInput(attrs={'class':'form-control'}))
    image = forms.URLField(max_length=500, required=False, label="Image URL (optional)",widget=forms.URLInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=[(category.categoryName, category.categoryName) for category in Categories.objects.all()], required=False, label="Category", widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Auctions
        fields = ['title','description','startingBid','image', 'category']

