from staff.models import Staff

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone

class CreateCourseViewTest(TestCase):

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

    def test_create_course_without_login(self):
        response = self.client.get(reverse('create_course'))
        self.assertRedirects(response,
                             '/account/login/?next=/academicInfo/createCourse/')

    def test_create_course_without_admin(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('create_course'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_create_course_with_admin(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        response = c.get(reverse('create_course'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'academicInfo/create_course.html')

    def test_post_request_with_invalid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_course'),
                          {'name' : 'Course',
                           'code': 'Code',
                           'credits': 10
                           }
                          )

        self.assertTemplateUsed(response, 'academicInfo/create_course.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'create_course_form', 'credits',
                             'Ensure this value is less than or equal to 8.')

    def test_post_request_with_valid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_course'),
                          {'name' : 'Course',
                           'code': 'Code',
                           'credits': 4
                           }
                          )

        self.assertTemplateUsed(response, 'academicInfo/create_course.html')
        self.assertEqual(response.status_code, 200)

    def test_view_courses_with_admin(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.get(reverse('view_course'))

        self.assertTemplateUsed(response, 'academicInfo/courses.html')
        self.assertEqual(response.status_code, 200)

    def test_view_course_without_admin(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('view_course'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
