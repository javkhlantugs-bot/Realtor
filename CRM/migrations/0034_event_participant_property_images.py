# Generated by Django 5.0 on 2024-02-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0033_notification_is_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participant_property_images',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True),
        ),
    ]