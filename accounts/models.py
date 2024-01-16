# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, PhoneNumberFormat

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=False)
    # Add other fields as needed

    def __str__(self):
        return self.username