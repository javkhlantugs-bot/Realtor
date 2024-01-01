from django.db import models
from Realtor.models import Property
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Clent(models.Model):
    client_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField()
    link = models.CharField(max_length=8, unique=True, blank=True)

    def __str__(self):
        return f"{self.client_name} - {self.phone_number} - {self.email}"

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        unique_id = str(uuid.uuid4().hex)[:8]
        while Clent.objects.filter(link=unique_id).exists():
            unique_id = str(uuid.uuid4().hex)[:8]
        return unique_id

class Client_suggestion(models.Model):
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
    file = models.FileField(upload_to='property_images/')

    def __str__(self):
        return f"{self.property} - {self.file}"
    

@receiver(post_save, sender=Clent)
def create_client_suggestions(sender, instance, created, **kwargs):
    if created:
        properties = Property.objects.all()
        for property in properties:
            Client_suggestion.objects.create(client=instance, property=property)

@receiver(post_save, sender=Property)
def create_property_suggestions(sender, instance, created, **kwargs):
    if created:
        clients = Clent.objects.all()
        for client in clients:
            Client_suggestion.objects.create(client=client, property=instance)