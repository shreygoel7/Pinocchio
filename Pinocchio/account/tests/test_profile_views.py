from academicInfo.models import Department

from staff.models import Staff

from student.models import Student

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone


class StudentProfileTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now().today()
        department = Department.objects.create(name='test department')
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
        self.student = Student.objects.create(
            user=user2,
            dob=startTime,
            department=department,
            batch=2018
        )

    def test_profile_not_student(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        response = c.get(reverse('profile'))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_profile_student(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('profile'))

        self.assertTemplateUsed(response, 'account/profile.html')
        self.assertEqual(response.status_code, 200)
