# Generated by Django 5.0 on 2024-01-03 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0004_delete_auto_suggestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='clent',
            name='is_searching',
            field=models.CharField(choices=[('looking_for_property', 'Looking For Property'), ('not_looking_for_property', 'Not Looking For Property')], max_length=50, null=True),
        ),
    ]
