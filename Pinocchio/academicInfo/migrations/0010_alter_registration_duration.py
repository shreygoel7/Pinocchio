# Generated by Django 3.2.9 on 2021-11-24 14:36

import academicInfo.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academicInfo', '0009_registration_endtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='duration',
            field=models.DurationField(),
        ),
    ]
