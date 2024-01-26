# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, PhoneNumberFormat

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=False)
    active = models.BooleanField(default = False)
    # Add other fields as needed

    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    # Add additional fields for the user profile

    def __str__(self):
        return self.user.username