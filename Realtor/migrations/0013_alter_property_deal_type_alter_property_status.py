# Generated by Django 5.0 on 2024-02-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Realtor', '0012_alter_property_property_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='deal_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
