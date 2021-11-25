# Generated by Django 3.2.9 on 2021-11-20 06:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.PositiveIntegerField(default=2021, validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(2000)]),
        ),
    ]