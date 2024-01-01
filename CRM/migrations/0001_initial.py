# Generated by Django 5.0 on 2023-12-29 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Realtor', '0001_initial'),
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
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='property_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Client_suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_suggested', models.CharField(choices=[('suggested', 'SUGGESTED'), ('not_suggested', 'NOT SUGGESTED')], default='not_suggested', max_length=50)),
                ('is_interested', models.CharField(choices=[('interested', 'INTERESTED'), ('not_interested', 'NOT INTERESTED')], default='not_interested', max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_suggestions', to='CRM.clent')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_suggestions', to='Realtor.property')),
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
                ('participant_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_bought', to='CRM.clent')),
                ('participant_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_owned', to='CRM.clent')),
                ('participant_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='Realtor.property')),
            ],
        ),
    ]
