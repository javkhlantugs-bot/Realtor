# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import parse, PhoneNumberFormat
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=False)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    ending_date = models.DateField(null=True, blank=True)
    # Add other fields as needed

    def __str__(self):
        return self.username
    
    
class UserPayment(models.Model):
    app_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
