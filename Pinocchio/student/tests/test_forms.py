from academicInfo.models import Department

from student.forms import StudentSignupForm
from student.models import Student

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class StudentSignupFormTest(TestCase):

    def test_signup_form_label(self):
        form = StudentSignupForm()
        self.assertTrue(
            form.fields['first_name'].label == 'First Name' and
            form.fields['last_name'].label == 'Last Name' and
            form.fields['username'].label == 'Roll number' and
            form.fields['dob'].label == 'Date of Birth' and
            form.fields['department'].label == 'Department' and
            form.fields['batch'].label == 'Batch' and
            form.fields['email'].label == 'Email'
        )

    def test_signup_form_required_fields(self):
        form = StudentSignupForm()
        self.assertTrue(
            form.fields['first_name'].required == True and
            form.fields['last_name'].required == True and
            form.fields['dob'].required == True and
            form.fields['department'].required == True and
            form.fields['batch'].required == True and
            form.fields['email'].required == True
        )

    def test_email_validation(self):

        startTime = timezone.now()
        department = Department.objects.create(name='test department')
        user = User.objects.create(
            username='test',
            email='test@gmail.com'
        )
        student = Student.objects.create(
            user=user,
            dob=startTime,
            batch=2018,
            department=department
        )

        form = StudentSignupForm(
            data = {
                'username': 'test1',
                'email': 'test@gmail.com',
                'dob': startTime,
                'batch': 2018,
                'department': department
            }
        )
        self.assertFalse(form.is_valid())

    def test_batch_lower_range(self):

        startTime = timezone.now()
        department = Department.objects.create(name='test department')

        form = StudentSignupForm(
            data = {
                'username': 'test1',
                'email': 'test@gmail.com',
                'dob': startTime,
                'batch': 1999,
                'department': department
            }
        )
        self.assertFalse(form.is_valid())

    def test_batch_upper_range(self):

        startTime = timezone.now()
        department = Department.objects.create(name='test department')

        form = StudentSignupForm(
            data = {
                'username': 'test1',
                'email': 'test@gmail.com',
                'dob': startTime,
                'batch': 10000,
                'department': department
            }
        )
        self.assertFalse(form.is_valid())
