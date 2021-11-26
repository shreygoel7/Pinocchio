from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Student(models.Model):
    """
     - Student model for student account.
     - Student should have roll number as username.
     - Student should have date of birth.
     - Student should have joining year as batch.
     - Student should be associated with a Department.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=False)
    batch = models.PositiveIntegerField(default=2021, blank=False,
                                        validators=[MaxValueValidator(9999), MinValueValidator(2000)]
                                        )
    department = models.ForeignKey('academicInfo.Department',
                                   on_delete=models.PROTECT)

    """
     - To get student's current semester.
     - Months 1-6 are even semesters and months 7-12 are odd semesters.
     - Calculated using formula:
     - (Current year - student joining year) x 2 + 1 if it is odd semester month
    """
    @property
    def get_student_semester(self):
        year = int(timezone.localdate().year)
        month = int(timezone.localdate().month)
        return (year - self.batch)*2 + 1 if month > 6 else 0

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
