from django.db import models
from Realtor.models import Property
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from accounts.models import CustomUser
from django.utils import timezone
from django.db.models.signals import pre_save

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Clent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField()
    link = models.CharField(max_length=8, unique=True, blank=True)

    status_choices = (
        ('looking_for_property', 'Looking For Property'),
        ('looking_for_rental_property', 'Looking For Rental'),
        ('selling_property', 'Selling property'),
        ('renting_Property', 'Renting Property'),
        ('tenant', 'Tenant'),
        ('inactive', 'Inactive'),
    )
    status = models.CharField(choices=status_choices, max_length=50, null=True)

    def __str__(self):
        return f"{self.client_name} - {self.phone_number} - {self.email}"

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = self.generate_unique_id()
        super().save(*args, **kwargs)

        # Check if the status has changed
        if self.pk is not None:
            old_instance = Clent.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                self.last_status_change = timezone.now()
                self.previous_status = old_instance.status

                # Create a StatusChangeLog entry
                StatusChangeLog.objects.create(
                    clent=self,
                    changed_date=self.last_status_change,
                    previous_status=self.previous_status,
                    new_status=self.status
                )

    def generate_unique_id(self):
        unique_id = str(uuid.uuid4().hex)[:8]
        while Clent.objects.filter(link=unique_id).exists():
            unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id

class StatusChangeLog(models.Model):
    client = models.ForeignKey(Clent, on_delete=models.CASCADE)
    changed_date = models.DateTimeField()
    previous_status = models.CharField(max_length=50)
    new_status = models.CharField(max_length=50)

class Client_suggestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client = models.ForeignKey(Clent, on_delete=models.CASCADE, related_name='client_suggestions')    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_suggestions')  
    SUGGESTION_CHOICES = (
        ('suggested', 'SUGGESTED'),
        ('not_suggested', 'NOT SUGGESTED')
    )
    INTERESTED_CHOICES = (
        ('interested', 'INTERESTED'),
        ('not_interested', 'NOT INTERESTED')
    )
    is_suggested = models.CharField(default="not_suggested", choices=SUGGESTION_CHOICES, max_length=50)
    is_interested = models.CharField(default='not_interested', choices=INTERESTED_CHOICES, max_length=50)

    def client_link(self):
        return self.client.link

    def __str__(self):
        return f"{self.client} - {self.property} - {self.is_suggested} - {self.is_interested} - {self.client_link()}"

class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    EVENT_TYPES = (
        ('meeting', 'Meeting'),
        ('show_property', 'Show Property'),
        ('sign_contract', 'Sign Contract'),
    )
    event_type = models.CharField(max_length=255, choices=EVENT_TYPES)
    event_date = models.DateField()
    event_time = models.TimeField(null=True)
    participant_buyer = models.ForeignKey(Clent, on_delete=models.CASCADE, related_name='events_bought')
    participant_owner = models.ForeignKey(Clent, on_delete=models.CASCADE, related_name='events_owned')
    event_description = models.TextField()
    participant_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property')
    

    def __str__(self):
        return f"{self.event_type} - {self.event_date} - {self.participant_buyer} - {self.participant_owner}"

class Files(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property} - {self.file}"
    

@receiver(post_save, sender=Clent)
def create_client_suggestions(sender, instance, created, **kwargs):
    if created:
        properties = Property.objects.filter(user=instance.user)
        for property in properties:
            Client_suggestion.objects.create(client=instance, property=property, user=instance.user)

@receiver(post_save, sender=Property)
def create_property_suggestions(sender, instance, created, **kwargs):
    if created:
        clients = Clent.objects.filter(user=instance.user)
        for client in clients:
            Client_suggestion.objects.create(client=client, property=instance, user = instance.user)




class ClientInterest(models.Model):
    PROPERTY_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('office', 'Office'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('loan', 'Loan'),
        ('leasing', 'Leasing'),
        ('all', 'All'),
    ]

    VIEW_SIGHT_CHOICES = [
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_CHOICES, null=True, blank=True)
    totalrooms = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    toilets = models.IntegerField(null=True, blank=True)
    min_floor_preference = models.IntegerField(null=True, blank=True)
    max_floor_preference = models.IntegerField(null=True, blank=True)
    min_square_meter = models.FloatField(null=True, blank=True)
    max_square_meter = models.FloatField(null=True, blank=True)
    payment_term = models.CharField(max_length=10, choices=PAYMENT_CHOICES, null=True, blank=True)
    min_price_range = models.CharField(max_length=20, null=True, blank=True)
    max_price_range = models.CharField(max_length=20, null=True, blank=True)
    view_sight = models.CharField(max_length=10, choices=VIEW_SIGHT_CHOICES, null=True, blank=True)
    date_added = models.DateField(null=True)

    # Add more fields based on additional details you want to include
    # Example: 
    additional_feature = models.CharField(max_length=50, null=True, blank=True)
    # ...

    # Add other necessary fields such as ForeignKey to link to a Client model
    client = models.ForeignKey(Clent, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Interest: {self.property_type}, Payment: {self.payment_term}, View Sight: {self.view_sight}"
