from academicInfo.models import Registration, Course, Department

from faculty.models import Faculty

from staff.models import Staff

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone

import datetime

class CreateCourseRegistrationViewTest(TestCase):

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

        startTime = timezone.now() + datetime.timedelta(days=1)
        timedelta = datetime.timedelta(days=1)
        endTime = startTime+timedelta
        self.registration = Registration.objects.create(name='Test Registration',
                                                        startTime=startTime,
                                                        duration=timedelta,
                                                        endTime=endTime)

        self.course = Course.objects.create(name='Test Course', code='TestCode',
                                            credits=4)
        department = Department.objects.create(name='test department')
        user = User.objects.create_user(username='testuser',
                                        password='complex1password',
                                        email='test@gmail.com')
        self.faculty = Faculty.objects.create(user=user, dob=startTime,
                                              department=department)

    def test_create_course_registration_without_login(self):
        response = self.client.get(reverse('create_course_registration'))
        self.assertRedirects(response,
                             '/account/login/?next=/academicInfo/createCourseRegistration/')

    def test_create_course_registration_without_admin(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('create_course_registration'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_create_course_registration_with_admin(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        response = c.get(reverse('create_course_registration'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response,
                                'academicInfo/create_course_registration.html')

    def test_post_request_with_invalid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_course_registration'),
                          {
                           'registration' : self.registration,
                           'course': self.course,
                           'faculty': self.faculty,
                           'capacity': 0,
                           'semester': 9
                           }
                          )

        self.assertTemplateUsed(response,
                                'academicInfo/create_course_registration.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'create_course_registration_form',
                             'capacity',
                             'Ensure this value is greater than or equal to 1.')
        self.assertFormError(response, 'create_course_registration_form',
                             'semester',
                             'Ensure this value is less than or equal to 8.')

    def test_post_request_with_valid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_course_registration'),
                          {
                           'registration' : self.registration.id,
                           'course': self.course.id,
                           'faculty': self.faculty.id,
                           'capacity': 30,
                           'semester': 5
                           }
                          )
        
        self.assertTemplateUsed(response,
                                'academicInfo/create_course_registration.html')
        self.assertEqual(response.status_code, 200)
