# Generated by Django 5.0 on 2024-01-25 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0022_client_status_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='clent',
            name='google_resource_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]