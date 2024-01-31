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
import datetime

class client_status_types(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length = 255)

    def __str__(self):
        return f"{self.status}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Clent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    link = models.CharField(max_length=8, unique=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    wedding_anniversary = models.DateField(null=True, blank=True)
    home_anniversary = models.DateField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    google_resource_id = models.CharField(null=True,blank = True, max_length= 255)
  
    status = models.ForeignKey(client_status_types, max_length=50, null=True, blank=True, on_delete=models.DO_NOTHING)

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

class client_relationships(models.Model):
    user = models.ForeignKey(Clent,on_delete=models.CASCADE)
    relationship_choices = (
        ('husband', 'Husband'),
        ('wife', 'Wife'),
        ('son', 'Son'),
        ('daughter', 'Daughter'),
        ('friend', 'Friend'),
        ('colleague', 'Colleague'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=255, null=True,blank=True)
    phone_number = models.CharField(max_length=30,null=True,blank=True)
    relationship_type = models.CharField(choices=relationship_choices, max_length = 255)

    def __str__(self):
        return f"{self.user} - {self.phone_number} - {self.name}- {self.relationship_type}"

class client_phone_numbers(models.Model):
    user = models.ForeignKey(Clent, on_delete = models.CASCADE)
    phone_types_choices = (
        ('work', 'Work'),
        ('home', 'Home'),
        ('mobile', 'Mobile'),
        ('fax', 'Fax'),
        ('other', 'Other'),
    )
    phone_type = models.CharField(choices = phone_types_choices, max_length = 255)
    phone_number = models.CharField(max_length=16) 
    def __str__(self):
        return f"{self.user} - {self.phone_type} - {self.phone_number}"

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

class event_type_model(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_type = models.CharField(max_length = 255)

    def __str__(self):
        return f"{self.event_type}"

class Event(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    event_hour_choice = (
        ('01','01'),
        ('02','02'),
        ('03','03'),
        ('04','04'),
        ('05','05'),
        ('06','06'),
        ('07','07'),
        ('08','08'),
        ('09','09'),
        ('10','10'),
        ('11','11'),
        ('12','12'),
    )
    event_minute_choice = (
        ('00','00'),
        ('15','15'),
        ('30','30'),
        ('45','45'),
    )
    event_ampm_choice = (
        ('am','AM'),
        ('am','PM'),
    )

    
    event_type = models.ForeignKey(event_type_model,max_length=255, null=True, blank=True,on_delete = models.DO_NOTHING, related_name = 'events_types')
    event_date = models.DateField()
    event_hour = models.CharField(null=True, blank=True, max_length = 5, choices = event_hour_choice)
    event_minute = models.CharField(null=True, blank=True, max_length = 5, choices = event_minute_choice)
    event_ampm = models.CharField(null=True, blank=True, max_length = 5, choices = event_ampm_choice)
    participant_buyer = models.ForeignKey(Clent, on_delete=models.CASCADE, related_name='events_bought', null=True,blank=True)
    participant_owner = models.ForeignKey(Clent, on_delete=models.CASCADE, related_name='events_owned', null=True,blank=True)
    event_description = models.TextField(null=True,blank=True)
    participant_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property', null=True,blank=True)
    is_completed = models.BooleanField(default = False) 
    participant_owner_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    participant_buyer_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    participant_property_address = models.CharField(max_length=255, null=True, blank=True, editable=False)
    event_type_name = models.CharField(max_length=255, null=True, blank=True, editable=False)
    index_field = models.DateTimeField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        # Convert date, hour, minute, am/pm to a datetime object
        if self.event_type:
            self.event_type_name = self.event_type.event_type

        # Save participant_owner's client name
        if self.participant_owner:
            self.participant_owner_name = self.participant_owner.client_name

        # Save participant_buyer's client name
        if self.participant_buyer:
            self.participant_buyer_name = self.participant_buyer.client_name

        if self.participant_property:
            self.participant_property_address = self.participant_property.address


        if self.event_date:
            hour = int(self.event_hour) if self.event_hour else 0
            minute = int(self.event_minute) if self.event_minute else 0
            am_pm = self.event_ampm if self.event_ampm else 'AM'

            if am_pm.upper() == 'PM' and hour != 12:
                hour += 12

            index_field_value = datetime.datetime.combine(self.event_date, datetime.time(hour, minute))
            self.index_field = index_field_value

        super().save(*args, **kwargs)

    @property
    def locations(self):
        if self.participant_property:
            return {
                'latitude': self.participant_property.latitude,
                'longitude': self.participant_property.longitude,
                'id': self.participant_property.id,
            }
        else:
            return None

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
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Add other necessary fields such as ForeignKey to link to a Client model
    client = models.ForeignKey(Clent, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Client: {self.client}"

class suggestion_link_settings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    contacts = models.CharField(max_length=50, blank=True, null=True)
    welcome_message = models.CharField(max_length=50, blank=True, null=True)

@receiver(post_save, sender=CustomUser)
def create_suggestion_link_settings(sender, instance, created, **kwargs):
    if created:
        suggestion_link_settings.objects.create(user=instance)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    property = models.ForeignKey(Property, on_delete= models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Clent, on_delete= models.CASCADE, null=True, blank=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.message} - {self.timestamp}"

def create_notification(sender, instance, **kwargs):
    if instance.is_interested == 'interested':
        notification_message = f"{instance.client.client_name} is interested in {instance.property.address}"
        Notification.objects.create(
            user=instance.user,
            message=notification_message,
            client=instance.client,
            property=instance.property
        )

# Connect the signal to the create_notification function
models.signals.post_save.connect(create_notification, sender=Client_suggestion)