# Generated by Django 5.0 on 2024-01-02 05:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CRM', '0001_initial'),
        ('Realtor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='clent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client_suggestion',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_suggestions', to='CRM.clent'),
        ),
        migrations.AddField(
            model_name='client_suggestion',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_suggestions', to='Realtor.property'),
        ),
        migrations.AddField(
            model_name='client_suggestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='clientinterest',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CRM.clent'),
        ),
        migrations.AddField(
            model_name='clientinterest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='participant_buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_bought', to='CRM.clent'),
        ),
        migrations.AddField(
            model_name='event',
            name='participant_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events_owned', to='CRM.clent'),
        ),
        migrations.AddField(
            model_name='event',
            name='participant_property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='Realtor.property'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='files',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
