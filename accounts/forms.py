# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser
from phonenumber_field.formfields import PhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number'}))
    accept_policies = forms.BooleanField(label='I accept the Privacy Policy and Terms of Service', required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }
    
class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'password','remember_me']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

class CustomUserChangeForm(UserChangeForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Phone Number'}), required=False)
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'phone_number','instagram_url'
                    ,'facebook_url'
                    ,'twitter_url'
                    ,'linkedin_url']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

class CustomUserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser

