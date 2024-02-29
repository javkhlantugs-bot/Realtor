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
        
        deal_type.objects.create(user=instance, deal_type="Rental")
        deal_type.objects.create(user=instance, deal_type="Sales")

        subscription_start_date = django.utils.timezone.now().date()
        subscription_end_date = subscription_start_date + relativedelta(days=14)
        UserPayment.objects.create(app_user=instance, subscription_start_date=subscription_start_date, subscription_end_date=subscription_end_date)

@receiver(post_save, sender=UserPayment)
def update_user_subscription(sender, instance, created, **kwargs):
    if created:
        # Assuming CustomUser has a ForeignKey to UserPayment
        instance.app_user.ending_date = instance.subscription_end_date
        instance.app_user.save()

import qrcode
import os 
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        # Construct the URL for the user
        user_url = f"estates.solutions/card/{instance.username}"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(user_url)
        qr.make(fit=True)

        # Save the QR code image
        qr_directory = os.path.join(settings.BASE_DIR, 'assets','static' ,'qr')
        os.makedirs(qr_directory, exist_ok=True)

        # Save the QR code image in the assets/qr directory
        file_name = f"qrcode_{instance.username}.png"
        file_path = os.path.join(qr_directory, file_name)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file_path)

        # You can optionally save the file path to the CustomUser model
        instance.qr_code = file_path
        instance.save()