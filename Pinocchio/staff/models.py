from django.contrib.auth.models import User
from django.db import models


class Staff(models.Model):
    """
     - Staff model for staff account.
     - Staff should have a date of birth.
     - Staff shoulf have is_admin boolean field.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
