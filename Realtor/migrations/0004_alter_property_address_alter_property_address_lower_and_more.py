# Generated by Django 5.0 on 2024-01-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Realtor', '0003_alter_property_condition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='address_lower',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bedrooms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='condition',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='deal_type',
            field=models.CharField(blank=True, choices=[('rental', 'Rental'), ('selling', 'Selling')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='property',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_month',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='price_sqrm',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='property_type',
            field=models.CharField(blank=True, choices=[('office', 'Office'), ('apartment', 'Apartment'), ('house', 'House')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='sqr_meter',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='toilets',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_floor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='total_rooms',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='which_floor',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
