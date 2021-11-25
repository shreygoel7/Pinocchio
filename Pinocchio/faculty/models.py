from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    department = models.ForeignKey('academicInfo.Department', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
