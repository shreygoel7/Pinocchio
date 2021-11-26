from staff.models import Staff

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client, TestCase
from django.utils import timezone

class CreateDepartmentViewTest(TestCase):

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

    def test_create_department_without_login(self):
        response = self.client.get(reverse('create_department'))
        self.assertRedirects(response,
                             '/account/login/?next=/academicInfo/createDepartment/')

    def test_create_department_without_admin(self):
        c = Client()
        login = c.login(username='test2', password='complex2password')
        response = c.get(reverse('create_department'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_create_department_with_admin(self):
        c = Client()
        login = c.login(username='test', password='complex1password')
        response = c.get(reverse('create_department'))

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'academicInfo/create_department.html')

    def test_post_request_with_invalid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_department'), {})

        self.assertTemplateUsed(response, 'academicInfo/create_department.html')
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'create_department_form',
                             'name', 'This field is required.')

    def test_post_request_with_valid_form(self):
        c = Client()
        login = c.login(username='test', password='complex1password')

        response = c.post(reverse('create_department'), {'name' : 'Department'})

        self.assertTemplateUsed(response, 'academicInfo/create_department.html')
        self.assertEqual(response.status_code, 200)
