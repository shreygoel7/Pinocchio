from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=False)
    batch = models.PositiveIntegerField(default=2021, blank=False, validators=[MaxValueValidator(9999), MinValueValidator(2000)])
    department = models.ForeignKey('academicInfo.Department', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
