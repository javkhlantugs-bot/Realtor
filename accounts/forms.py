# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from cities_light.models import Country, City
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control','hx-get':'load_cities/','hx-target':'#id_city'}))
    city = forms.ModelChoiceField(queryset=City.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'country', 'city']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            # 'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
