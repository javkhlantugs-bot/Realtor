# Generated by Django 5.0 on 2024-01-02 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('link', models.CharField(blank=True, max_length=8, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Client_suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_suggested', models.CharField(choices=[('suggested', 'SUGGESTED'), ('not_suggested', 'NOT SUGGESTED')], default='not_suggested', max_length=50)),
                ('is_interested', models.CharField(choices=[('interested', 'INTERESTED'), ('not_interested', 'NOT INTERESTED')], default='not_interested', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.CharField(blank=True, choices=[('house', 'House'), ('apartment', 'Apartment'), ('office', 'Office')], max_length=20, null=True)),
                ('rooms', models.IntegerField(blank=True, null=True)),
                ('floor_preference', models.IntegerField(blank=True, null=True)),
                ('square_meter', models.FloatField(blank=True, null=True)),
                ('payment_term', models.CharField(blank=True, choices=[('cash', 'Cash'), ('loan', 'Loan'), ('leasing', 'Leasing')], max_length=10, null=True)),
                ('price_range', models.CharField(blank=True, max_length=20, null=True)),
                ('view_sight', models.CharField(blank=True, choices=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], max_length=10, null=True)),
                ('date_added', models.DateField(null=True)),
                ('additional_feature', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('meeting', 'Meeting'), ('show_property', 'Show Property'), ('sign_contract', 'Sign Contract')], max_length=255)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField(null=True)),
                ('event_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='property_images/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
