from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Course, CourseRegistration, Registration

class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Course Name'
        self.fields['code'].label = 'Course Code'
        self.fields['credits'].label = 'Course Credits'

class CreateCourseRegistrationForm(forms.ModelForm):

    class Meta:
        model = CourseRegistration
        fields = ('registration', 'course', 'faculty', 'capacity', 'semester',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['registration'].label = 'Registration'
        self.fields['course'].label = 'Course'
        self.fields['faculty'].label = 'Faculty'
        self.fields['capacity'].label = 'Capacity'
        self.fields['semester'].label = 'Semester'

        # Allow create course registration only for future registrations
        self.fields['registration'].queryset = Registration.objects.filter(startTime__gt=timezone.now())

class CreateRegistrationForm(forms.ModelForm):

    class Meta:
        model = Registration
        fields = ('name','startTime',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Registration Name'
        self.fields['startTime'].label = 'Registration Start Time'
