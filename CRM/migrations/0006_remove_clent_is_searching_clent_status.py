# Generated by Django 5.0 on 2024-01-03 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0005_clent_is_searching'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clent',
            name='is_searching',
        ),
        migrations.AddField(
            model_name='clent',
            name='status',
            field=models.CharField(choices=[('looking_for_property', 'Looking For Property'), ('looking_for_rental_property', 'Looking For Rental'), ('selling_property', 'Selling property'), ('Renting Property', 'Renting Property')], max_length=50, null=True),
        ),
    ]
