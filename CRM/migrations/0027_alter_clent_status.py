# Generated by Django 5.0 on 2024-01-31 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0026_search_remove_suggestion_link_settings_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clent',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]