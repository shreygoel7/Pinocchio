# Generated by Django 3.2.9 on 2021-11-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academicInfo', '0011_alter_registration_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]