from academicInfo.models import Department

from staff.models import Staff

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone


class FacultySignUpTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now()
        user1 = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='complex1password'
        )
        user2 = User.objects.create_user(
            username='test2',
            email='tes2t@gmail.com',
            password='complex2password'
        )
        self.staff1 = Staff.objects.create(
            user=user1,
            dob=startTime,
            is_admin=True,
        )
        self.staff2 = Staff.objects.create(
            user=user2,
            dob=startTime,
            is_admin=False,
        )

    def test_faculty_signup_with_login(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('faculty_sign_up'))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_faculty_signup_without_login(self):
        c = Client()

        response = c.get(reverse('faculty_sign_up'))

        self.assertTemplateUsed(response, 'account/faculty_signup.html')
        self.assertEqual(response.status_code, 200)

    def test_post_faculty_valid(self):
        c = Client()

        startTime = timezone.now().date()
        department = Department.objects.create(name='test department')

        response = c.post(reverse('faculty_sign_up'),{'username': 'test12',
                                                      'first_name': 'Bob',
                                                      'last_name': 'Davidson',
                                                      'dob': startTime,
                                                      'email': 'test3@gmail.com',
                                                      'password1': 'complex1password',
                                                      'password2': 'complex1password',
                                                      'department': department.id})

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)

    def test_post_faculty_invalid(self):
        c = Client()

        startTime = timezone.now().date()
        department = Department.objects.create(name='test department')

        response = c.post(reverse('faculty_sign_up'),{'username': 'test',
                                                      'first_name': 'Bob',
                                                      'last_name': 'Davidson',
                                                      'dob': startTime,
                                                      'email': 'test@gmail.com',
                                                      'password1': 'complex1password',
                                                      'password2': 'complex1password',
                                                      'department': department.id})

        self.assertTemplateUsed(response, 'account/faculty_signup.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'faculty_signup_form', 'username',
                             'A user with that username already exists.')
        self.assertFormError(response, 'faculty_signup_form', 'email',
                             'Email already exists')

class StaffSignUpTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now()
        user1 = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='complex1password'
        )
        user2 = User.objects.create_user(
            username='test2',
            email='tes2t@gmail.com',
            password='complex2password'
        )
        self.staff1 = Staff.objects.create(
            user=user1,
            dob=startTime,
            is_admin=True,
        )
        self.staff2 = Staff.objects.create(
            user=user2,
            dob=startTime,
            is_admin=False,
        )

    def test_staff_signup_with_login(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('staff_sign_up'))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_staff_signup_without_login(self):
        c = Client()

        response = c.get(reverse('staff_sign_up'))

        self.assertTemplateUsed(response, 'account/staff_signup.html')
        self.assertEqual(response.status_code, 200)

    def test_post_staff_valid(self):
        c = Client()

        startTime = timezone.now().date()

        response = c.post(reverse('staff_sign_up'),{'username': 'test12',
                                                    'first_name': 'Bob',
                                                    'last_name': 'Davidson',
                                                    'dob': startTime,
                                                    'email': 'test3@gmail.com',
                                                    'password1': 'complex1password',
                                                    'password2': 'complex1password'})

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)

    def test_post_staff_invalid(self):
        c = Client()

        startTime = timezone.now().date()

        response = c.post(reverse('staff_sign_up'),{'username': 'test',
                                                    'first_name': 'Bob',
                                                    'last_name': 'Davidson',
                                                    'dob': startTime,
                                                    'email': 'test@gmail.com',
                                                    'password1': 'complex1password',
                                                    'password2': 'complex1password'})

        self.assertTemplateUsed(response, 'account/staff_signup.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'staff_signup_form', 'username',
                             'A user with that username already exists.')
        self.assertFormError(response, 'staff_signup_form', 'email',
                             'Email already exists')

class StudentSignUpTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now()
        user1 = User.objects.create_user(
            username='test',
            email='test@gmail.com',
            password='complex1password'
        )
        user2 = User.objects.create_user(
            username='test2',
            email='tes2t@gmail.com',
            password='complex2password'
        )
        self.staff1 = Staff.objects.create(
            user=user1,
            dob=startTime,
            is_admin=True,
        )
        self.staff2 = Staff.objects.create(
            user=user2,
            dob=startTime,
            is_admin=False,
        )

    def test_student_signup_with_login(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('student_sign_up'))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_student_signup_without_login(self):
        c = Client()

        response = c.get(reverse('student_sign_up'))

        self.assertTemplateUsed(response, 'account/student_signup.html')
        self.assertEqual(response.status_code, 200)

    def test_post_student_valid(self):
        c = Client()

        startTime = timezone.now().date()
        department = Department.objects.create(name='test department')

        response = c.post(reverse('student_sign_up'),{'username': 'test12',
                                                      'first_name': 'Bob',
                                                      'last_name': 'Davidson',
                                                      'dob': startTime,
                                                      'email': 'test3@gmail.com',
                                                      'password1': 'complex1password',
                                                      'password2': 'complex1password',
                                                      'batch': 2018,
                                                      'department': department.id})

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)

    def test_post_student_invalid(self):
        c = Client()

        startTime = timezone.now().date()
        department = Department.objects.create(name='test department')

        response = c.post(reverse('student_sign_up'),{'username': 'test',
                                                      'first_name': 'Bob',
                                                      'last_name': 'Davidson',
                                                      'dob': startTime,
                                                      'email': 'test@gmail.com',
                                                      'password1': 'complex1password',
                                                      'password2': 'complex1password',
                                                      'batch': 2018,
                                                      'department': department.id})

        self.assertTemplateUsed(response, 'account/student_signup.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'student_signup_form', 'username',
                             'A user with that username already exists.')
        self.assertFormError(response, 'student_signup_form', 'email',
                             'Email already exists')

    def test_post_student_invalid_batch(self):
        c = Client()

        startTime = timezone.now().date()
        department = Department.objects.create(name='test department')

        response = c.post(reverse('student_sign_up'),{'username': 'test12',
                                                      'first_name': 'Bob',
                                                      'last_name': 'Davidson',
                                                      'dob': startTime,
                                                      'email': 'test3@gmail.com',
                                                      'password1': 'complex1password',
                                                      'password2': 'complex1password',
                                                      'batch': 9000,
                                                      'department': department.id})

        self.assertTemplateUsed(response, 'account/student_signup.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'student_signup_form', 'batch',
                             'This value cannot be greater than current year.')
