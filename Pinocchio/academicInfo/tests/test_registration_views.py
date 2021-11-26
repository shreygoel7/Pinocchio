from academicInfo.models import Course, Department, Registration, CourseRegistration
from academicInfo.forms import CreateRegistrationForm

from staff.models import Staff

from student.models import Student

from faculty.models import Faculty

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

    def test_create_registration_without_login(self):
        response = self.client.get(reverse('create_registration'))
        self.assertRedirects(response, '/account/login/?next=/academicInfo/createRegistration/')

    def test_create_registration_without_admin(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('create_registration'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 302)

        # Check we used correct template
        self.assertRedirects(response, '/')

    def test_create_registration_with_admin(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        response = c.get(reverse('create_registration'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'academicInfo/create_registration.html')

    def test_post_request_with_invalid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_registration'), {})

        self.assertTemplateUsed(response, 'academicInfo/create_registration.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'create_registration_form', 'name', 'This field is required.')

    def test_post_request_with_valid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_registration'), {'name' : 'Test',
                                                           'startTime': timezone.now()+datetime.timedelta(days=1),
                                                           'days': 2,
                                                           'hours': 0,
                                                           'minutes': 0
                                                           })
        self.assertTemplateUsed(response, 'academicInfo/create_registration.html')
        self.assertEqual(response.status_code, 200)

    def test_post_request_with_zero_duration(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_registration'), {'name' : 'Test',
                                                           'startTime': timezone.now()+datetime.timedelta(days=1),
                                                           'days': 0,
                                                           'hours': 0,
                                                           'minutes': 0
                                                           })
        self.assertTemplateUsed(response, 'academicInfo/create_registration.html')
        self.assertEqual(response.status_code, 200)

class RegistrationViewTest(TestCase):

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

    def test_registration_view(self):
        c = Client()

        response = c.get(reverse('registration'))

        self.assertTemplateUsed(response, 'academicInfo/registration.html')
        self.assertEqual(response.status_code, 200)

class LiveRegistrationViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        startTime = timezone.now()
        department = Department.objects.create(name='Test')
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
        self.student = Student.objects.create(
            user=user1,
            dob=startTime,
            batch=2018,
            department=department
        )
        startTime = timezone.now()
        timedelta = datetime.timedelta(days=1)
        endTime = startTime+timedelta
        self.registration = Registration.objects.create(name='Test Registration', startTime=startTime, duration=timedelta, endTime=endTime)
        self.course = Course.objects.create(name='Test Course', code='TestCode', credits=4)
        self.faculty = Faculty.objects.create(user=user2, dob=startTime, department=department)

    def test_live_registration_view_without_student(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')

        response = c.get(reverse('live_registration', kwargs={'registration_id':self.registration.id}))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_live_registration_view_for_student(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.get(reverse('live_registration', kwargs={'registration_id':self.registration.id}))

        self.assertTemplateUsed(response, 'academicInfo/live_registration.html')
        self.assertEqual(response.status_code, 200)

    def test_post_live_registration_for_student(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        course_registration = CourseRegistration.objects.create(registration=self.registration,
                                                                course=self.course,
                                                                faculty=self.faculty,
                                                                capacity=20,
                                                                semester=8
                                                                )

        response = c.post(reverse('live_registration', kwargs={'registration_id':self.registration.id}), {'Register': True,
                                                                                                          'course_registration_id': course_registration.id})

        self.assertEqual(response.status_code, 302)

    def test_post_live_registration_for_student_invalid(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        course_registration = CourseRegistration.objects.create(registration=self.registration,
                                                                course=self.course,
                                                                faculty=self.faculty,
                                                                capacity=20,
                                                                semester=3
                                                                )

        response = c.post(reverse('live_registration', kwargs={'registration_id':self.registration.id}), {'Register': True,
                                                                                                          'course_registration_id': course_registration.id})

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)

    def test_post_live_unregister_for_student(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        course_registration = CourseRegistration.objects.create(registration=self.registration,
                                                                course=self.course,
                                                                faculty=self.faculty,
                                                                capacity=20,
                                                                semester=8
                                                                )
        course_registration.students.add(self.student)

        response = c.post(reverse('live_registration', kwargs={'registration_id':self.registration.id}), {'UnRegister': True,
                                                                                                          'course_registration_id': course_registration.id})

        self.assertEqual(response.status_code, 302)

    def test_post_live_registration_view_without_student(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')

        response = c.post(reverse('live_registration', kwargs={'registration_id':self.registration.id}))

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 302)
