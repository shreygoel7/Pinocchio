from staff.models import Staff

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class StaffTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        startTime = timezone.now()
        self.user = User.objects.create_user(
            username='test_user',
            first_name='Bob',
            last_name='Davidson',
            password='complex1password'
        )
        self.staff = Staff.objects.create(
            user=self.user,
            dob=timezone.now(),
        )

    def test_student_name(self):
        expected_name = self.user.first_name + ' ' + self.user.last_name
        self.assertEqual(str(self.staff), expected_name)
