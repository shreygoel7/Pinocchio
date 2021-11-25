from academicInfo.models import Department
from student.models import Student

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class StudentTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        startTime = timezone.now()
        department = Department.objects.create(name='test department')
        self.user = User.objects.create(
            username='test_user',
            first_name='Bob',
            last_name='Davidson'
        )
        self.student = Student.objects.create(
            user=self.user,
            dob=timezone.now(),
            batch=2018,
            department=department
        )

    def test_student_name(self):
        expected_name = self.user.first_name + ' ' + self.user.last_name
        self.assertEqual(str(self.student), expected_name)
