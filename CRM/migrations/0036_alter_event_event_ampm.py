# Generated by Django 5.0 on 2024-02-07 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0035_alter_event_participant_property'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_ampm',
            field=models.CharField(blank=True, choices=[('am', 'AM'), ('pm', 'PM')], max_length=5, null=True),
        ),
    ]