# Generated by Django 5.0 on 2024-02-17 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0039_clientinterest_added_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientinterest',
            name='added_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
