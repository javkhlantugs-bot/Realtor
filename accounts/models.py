# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Address(models.Model):
   country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
   city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    country = models.CharField(max_length=100, null = True)
    city = models.CharField(max_length=100, null = True)
    # Add other fields as needed

    def __str__(self):
        return self.username