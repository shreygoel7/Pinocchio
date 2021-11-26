from academicInfo.models import Department

from student.models import Student

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone

import datetime

class AuthTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now().today()
        department = Department.objects.create(name='test department')
        user2 = User.objects.create_user(
            username='test2',
            email='tes2t@gmail.com',
            password='complex2password'
        )
        self.student = Student.objects.create(
            user=user2,
            dob=startTime,
            department=department,
            batch=2018
        )

    def test_already_login_view(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('login'))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_new_login_view_invalid(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'test2'})

        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'login_form', 'password', 'This field is required.')

    def test_new_login_view(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'test2',
                                            'password': 'complex2password'})

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_wrong_login_view(self):
        c = Client()
        response = c.post(reverse('login'), {'username': 'test23',
                                            'password': 'complex2password'})

        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)

    def test_post_logout(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.post(reverse('logout'))

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
