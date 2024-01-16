# Generated by Django 5.0 on 2024-01-11 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0012_alter_client_social_links_platform'),
    ]

    operations = [
        migrations.AddField(
            model_name='clent',
            name='facebook_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clent',
            name='instagram_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='clent',
            name='twitter_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='client_social_links',
        ),
    ]