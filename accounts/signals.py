from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from CRM.models import event_type_model, client_status_types, event_type_model
from Realtor.models import property_status, property_type, deal_type
from .models import CustomUser, UserPayment
import django.utils.timezone
from dateutil.relativedelta import relativedelta

@receiver(post_save, sender=CustomUser)
def create_user_objects(sender, instance, created, **kwargs):
    if created:
        # Create EventType records
        event_type_model.objects.create(user=instance, event_type="Meeting")
        event_type_model.objects.create(user=instance, event_type="Show property")

        # Create ClientStatusTypes records
        client_status_types.objects.create(user=instance, status="Investor")
        client_status_types.objects.create(user=instance, status="Tenant")
        client_status_types.objects.create(user=instance, status="Relative")
        client_status_types.objects.create(user=instance, status="Friend")

        # Create PropertyStatus records
        property_status.objects.create(user=instance, status="Sold")
        property_status.objects.create(user=instance, status="Cancelled")
        property_status.objects.create(user=instance, status="Ongoing")

        # Create PropertyType records
        property_type.objects.create(user=instance, type="Office")
        property_type.objects.create(user=instance, type="Land")
        property_type.objects.create(user=instance, type="Apartment")
        
        deal_type.objects.create(user=instance, type="Rental")
        deal_type.objects.create(user=instance, type="Sales")

        subscription_start_date = django.utils.timezone.now().date()
        subscription_end_date = subscription_start_date + relativedelta(days=14)
        UserPayment.objects.create(app_user=instance, subscription_start_date=subscription_start_date, subscription_end_date=subscription_end_date)

@receiver(post_save, sender=UserPayment)
def update_user_subscription(sender, instance, created, **kwargs):
    if created:
        # Assuming CustomUser has a ForeignKey to UserPayment
        instance.app_user.ending_date = instance.subscription_end_date
        instance.app_user.save()