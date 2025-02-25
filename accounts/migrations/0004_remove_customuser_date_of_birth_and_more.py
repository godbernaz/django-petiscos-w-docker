# Generated by Django 5.1.4 on 2025-01-23 15:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_address_customuser_city_customuser_nif_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_of_birth',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='nif',
            field=models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='O NIF deve conter exatamente 9 dígitos.', regex='^\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=9, null=True, validators=[django.core.validators.RegexValidator(message='O número de telemóvel deve conter exatamente 9 dígitos.', regex='^\\d{9}$')]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='postal_code',
            field=models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator(message='O código postal deve estar no formato XXXX-XXX.', regex='^\\d{4}-\\d{3}$')]),
        ),
    ]
