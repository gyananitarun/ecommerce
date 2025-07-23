from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'category', 'subcategory', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )

class FilterForm(forms.Form):
    PRICE_CHOICES = [
        ('', 'All Prices'),
        ('0-100', '0 - 100'),
        ('100-500', '100 - 500'),
        ('500-1000', '500 - 1000'),
        ('1000+', '1000+'),
    ]
    
    category = forms.ModelChoiceField(
        queryset=None,
        empty_label="All Categories",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    price_range = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        from .models import Category
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
