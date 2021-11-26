from academicInfo.models import (Course, Registration, CourseRegistration,
                                 Department)

from faculty.models import Faculty

from student.models import Student

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

import datetime

class CourseTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Course.objects.create(name='Test Course', code='TestCode', credits=4)

    def test_course_name(self):
        course = Course.objects.get(code='TestCode')
        expected_name = course.name
        self.assertEqual(str(course), expected_name)

class RegistrationTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        startTime = timezone.now()
        timedelta = datetime.timedelta(days=1)
        endTime = startTime+timedelta
        self.registration = Registration.objects.create(name='Test Registration',
                                                        startTime=startTime,
                                                        duration=timedelta,
                                                        endTime=endTime)

    def test_registration_name(self):
        expected_name = self.registration.name + ' on ' + (self.registration.startTime +
                                                           datetime.timedelta(hours=5, minutes=30)
                                                           ).strftime("%d %b, %Y  %I:%M:%S %p")
        self.assertEqual(str(self.registration), expected_name)

class CourseRegistrationTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        startTime = timezone.now()
        timedelta = datetime.timedelta(days=1)
        endTime = startTime+timedelta
        registration = Registration.objects.create(name='Test Registration',
                                                   startTime=startTime,
                                                   duration=timedelta,
                                                   endTime=endTime)
        course = Course.objects.create(name='Test Course', code='TestCode',
                                       credits=4)
        department = Department.objects.create(name='test department')
        user = User.objects.create(username='testuser')
        faculty = Faculty.objects.create(user=user, dob=startTime,
                                         department=department)
        user2 = User.objects.create(username='testStudent')
        student = Student.objects.create(user=user2, dob=startTime, batch=2018,
                                         department=department)
        self.course_registration = CourseRegistration.objects.create(registration=registration,
                                                                     course=course,
                                                                     faculty=faculty,
                                                                     capacity=20,
                                                                     semester=2
                                                                     )
        self.course_registration.students.add(student)

    def test_remaining_seats(self):
        expected_remaining_seats = (self.course_registration.capacity -
                                    self.course_registration.students.count())
        self.assertEqual(self.course_registration.remaining_seats,
                         expected_remaining_seats)

class DepartmentTest(TestCase):

    @classmethod
    def setUpTestData(self):
        self.department = Department.objects.create(name='test department')

    def test_department_name(self):
        expected_name = self.department.name
        self.assertEqual(str(self.department), expected_name)
