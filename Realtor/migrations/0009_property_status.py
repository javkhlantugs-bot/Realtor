# Generated by Django 5.0 on 2024-01-10 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Realtor', '0008_property_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('cancelled', 'Cancelled')], max_length=30, null=True),
        ),
    ]
