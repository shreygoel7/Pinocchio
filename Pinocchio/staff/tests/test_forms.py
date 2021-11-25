from staff.forms import StaffSignupForm
from staff.models import Staff

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class StaffSignupFormTest(TestCase):

    def test_signup_form_label(self):
        form = StaffSignupForm()
        self.assertTrue(
            form.fields['first_name'].label == 'First Name' and
            form.fields['last_name'].label == 'Last Name' and
            form.fields['username'].label == 'Username' and
            form.fields['dob'].label == 'Date of Birth' and
            form.fields['email'].label == 'Email'
        )

    def test_signup_form_required_fields(self):
        form = StaffSignupForm()
        self.assertTrue(
            form.fields['first_name'].required == True and
            form.fields['last_name'].required == True and
            form.fields['dob'].required == True and
            form.fields['email'].required == True
        )

    def test_invalid_email_validation(self):

        startTime = timezone.now()
        user = User.objects.create(
            username='test',
            email='test@gmail.com'
        )
        staff = Staff.objects.create(
            user=user,
            dob=startTime,
            is_admin=True,
        )

        form = StaffSignupForm(
            data = {
                'username': 'test1',
                'email': 'test@gmail.com',
                'dob': startTime
            }
        )
        self.assertFalse(form.is_valid())

    def test_valid_email_validation(self):

        startTime = timezone.now()

        form = StaffSignupForm(
            data = {
                'username': 'test',
                'first_name': 'Bob',
                'last_name': 'Davidson',
                'dob': startTime,
                'email': 'test@gmail.com',
                'password1': 'complex1password',
                'password2': 'complex1password'
            }
        )
        self.assertTrue(form.is_valid())
