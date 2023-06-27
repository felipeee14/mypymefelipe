from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Product

class ProductForm(forms.ModelForm):
    product_image = forms.ImageField(required=False, label='Imagen del producto', 
                                     widget=forms.FileInput(attrs={'class': 'form-control-file'}))

   
class Meta:
    model = Product
    fields = ['product_name', 'product_price', 'product_image', 'product_state']
    labels = {
        'product_name': 'Nombre del producto',
        'product_price': 'Precio del producto',
        'product_state': 'Estado del producto',
    }
    widgets = {
        'product_name': forms.TextInput(attrs={'class': 'form-control'}),
        'product_price': forms.NumberInput(attrs={'class': 'form-control'}),
        'product_state': forms.Select(attrs={'class': 'form-control'}),
        }