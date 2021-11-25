from academicInfo.forms import (CreateCourseForm, CreateRegistrationForm,
                                CreateCourseRegistrationForm)

from django.test import TestCase

class CourseFormTest(TestCase):

    def test_course_form_label(self):
        form = CreateCourseForm()
        self.assertTrue(
            form.fields['name'].label == 'Course Name' and
            form.fields['code'].label == 'Course Code' and
            form.fields['credits'].label == 'Course Credits'
        )

    def test_course_credit_lower_range(self):
        form = CreateCourseForm(
            data = {
                    'name': 'test',
                    'code': 'test code',
                    'credits': 0
            }
        )
        self.assertFalse(form.is_valid())

    def test_course_credit_upper_range(self):
        form = CreateCourseForm(
            data = {
                    'name': 'test',
                    'code': 'test code',
                    'credits': 9
            }
        )
        self.assertFalse(form.is_valid())

class CourseRegistrationFormTest(TestCase):

    def test_course_registration_form_label(self):
        form = CreateCourseRegistrationForm()
        self.assertTrue(
            form.fields['registration'].label == 'Registration' and
            form.fields['course'].label == 'Course' and
            form.fields['faculty'].label == 'Faculty' and
            form.fields['capacity'].label == 'Capacity' and
            form.fields['semester'].label == 'Semester'
        )

    def test_course_registration_capacity_lower_range(self):
        form = CreateCourseRegistrationForm(
            data = {
                'capacity' : 0
            }
        )
        self.assertFalse(form.is_valid())

    def test_course_registration_semester_lower_range(self):
        form = CreateCourseRegistrationForm(
            data = {
                'semester' : 0
            }
        )
        self.assertFalse(form.is_valid())

    def test_course_registration_semester_upper_range(self):
        form = CreateCourseRegistrationForm(
            data = {
                'semester' : 9
            }
        )
        self.assertFalse(form.is_valid())

class RegistrationFormTest(TestCase):

    def test_registration_form_label(self):
        form = CreateRegistrationForm()
        self.assertTrue(
            form.fields['name'].label == 'Registration Name' and
            form.fields['startTime'].label == 'Registration Start Time'
        )
