# Generated by Django 5.0 on 2024-01-31 04:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0029_alter_clent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clent',
            name='status',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='CRM.client_status_types'),
        ),
    ]