# Generated by Django 3.2.9 on 2021-11-23 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academicInfo', '0004_registration_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='startTime',
            field=models.DateTimeField(),
        ),
    ]
