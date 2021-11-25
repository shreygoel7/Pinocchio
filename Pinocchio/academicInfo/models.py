from faculty.models import Faculty
from student.models import Student
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import datetime

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    code = models.CharField(max_length=10, unique=True)
    credits = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(8)])

    def __str__(self):
        return self.name

class Registration(models.Model):
    name = models.CharField(max_length=100, blank=False)
    startTime = models.DateTimeField(blank=False)
    duration = models.DurationField(blank=False)
    endTime = models.DateTimeField(blank=False)

    def __str__(self):
        return self.name + ' on ' + (self.startTime + datetime.timedelta(hours=5, minutes=30)).strftime("%d %b, %Y  %I:%M:%S %p")

class CourseRegistration(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
    students = models.ManyToManyField(Student, blank=True)
    capacity = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1)])
    semester = models.PositiveIntegerField(blank=False, validators=[MinValueValidator(1), MaxValueValidator(8)])

    @property
    def remaining_seats(self):
        return self.capacity - self.students.count()

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
