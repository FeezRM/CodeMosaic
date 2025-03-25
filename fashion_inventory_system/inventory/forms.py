from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Product

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ProductFilterForm(forms.Form):
    search = forms.CharField(required=False, label='Search')
    brand = forms.CharField(required=False)
    category = forms.CharField(required=False)
    color = forms.CharField(required=False)
    size = forms.CharField(required=False)
    material = forms.CharField(required=False)
    price_min = forms.DecimalField(required=False, decimal_places=2)
    price_max = forms.DecimalField(required=False, decimal_places=2)
    stock_min = forms.IntegerField(required=False, label='Min Stock')