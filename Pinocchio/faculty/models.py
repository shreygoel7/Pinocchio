from django.contrib.auth.models import User
from django.db import models


class Faculty(models.Model):
    """
     - Faculty model for faculty account.
     - Faculty should have roll number as email.
     - Faculty should have date of birth.
     - Faculty should be associated with a Department.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    department = models.ForeignKey('academicInfo.Department',
                                   on_delete=models.PROTECT)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
