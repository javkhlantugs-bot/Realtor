# Generated by Django 5.0 on 2024-01-04 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0008_alter_clent_status_statuschangelog'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statuschangelog',
            old_name='clent',
            new_name='client',
        ),
    ]
