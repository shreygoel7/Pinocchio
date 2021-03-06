from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .forms import (CreateCourseForm,
                    CreateCourseRegistrationForm,
                    CreateDepartmentForm,
                    CreateRegistrationForm)

from .models import Course, CourseRegistration, Department, Registration

import datetime
from django.utils import timezone


class CreateCourseView(LoginRequiredMixin, View):
    """
    View for admin to create new Course.
    """

    template_name = 'academicInfo/create_course.html'
    create_course_form = CreateCourseForm

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            create_course_form = self.create_course_form()
            return render(request, self.template_name, {'create_course_form' : create_course_form})
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        create_course_form = CreateCourseForm(request.POST)

        if create_course_form.is_valid():
            course = create_course_form.save()
            course.save()

            return redirect('view_course')

        return render(request, self.template_name, {'create_course_form' : create_course_form})


class CreateCourseRegistrationView(LoginRequiredMixin, View):
    """
    View for admin to add Course to the Registration.
    """

    template_name = 'academicInfo/create_course_registration.html'
    create_course_registration_form = CreateCourseRegistrationForm

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            create_course_registration_form = self.create_course_registration_form()
            return render(request, self.template_name, {'create_course_registration_form' : create_course_registration_form})
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        create_course_registration_form = CreateCourseRegistrationForm(request.POST)

        if create_course_registration_form.is_valid():

            # Add course to registration only if this course is not added already
            # in this registration.
            course_registration = create_course_registration_form.save(commit=False)

            # Check if the registration has already started.
            if course_registration.registration.startTime <= timezone.now():
                create_course_registration_form.add_error('registration',
                                                          'The registration has already started, you cannot add course to it now.')
                return render(request, self.template_name, {'create_course_registration_form' : create_course_registration_form})

            courses_in_registration = course_registration.registration.courseregistration_set.all()
            similar_course_registration = courses_in_registration.filter(course=course_registration.course,
                                                                         semester=course_registration.semester)

            # Check if course is not already present in the same registration and semester.
            if len(similar_course_registration) == 0:
                course_registration.save()
                return render(request, self.template_name, {'create_course_registration_form' : create_course_registration_form,
                                                            'success': 'Successfully added course to the registration.'})
            else:
                create_course_registration_form.add_error('course', 'This course is already added in this semester.')
                create_course_registration_form.add_error('semester', 'This semester already has this course.')

        return render(request, self.template_name, {'create_course_registration_form' : create_course_registration_form})


class CreateDepartmentView(LoginRequiredMixin, View):
    """
    View for admin to add new Department.
    """

    template_name = 'academicInfo/create_department.html'
    create_department_form = CreateDepartmentForm

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            create_department_form = self.create_department_form()
            return render(request, self.template_name, {'create_department_form' : create_department_form})
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        create_department_form = CreateDepartmentForm(request.POST)

        # Check if Department with same name does not already exist.
        if create_department_form.is_valid():
            department = create_department_form.save()
            department.save()
            return redirect('view_department')
        else:
            return render(request, self.template_name, {'create_department_form' : create_department_form})


class CreateRegistrationView(LoginRequiredMixin, View):
    """
    View for admin to create new Registration.
    """

    template_name = 'academicInfo/create_registration.html'
    create_registration_form = CreateRegistrationForm

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            create_registration_form = self.create_registration_form()
            return render(request, self.template_name, {'create_registration_form' : create_registration_form})
        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):
        create_registration_form = CreateRegistrationForm(request.POST)

        # Check if the Registration form is valid.
        if create_registration_form.is_valid():
            days = int(request.POST['days'])
            hours = int(request.POST['hours'])
            minutes = int(request.POST['minutes'])

            # Check if duration is 0 or not.
            if days + hours + minutes == 0:

                # Duration cannot be 0.
                return render(request, self.template_name, {'create_registration_form' : create_registration_form,
                                                            'error' : 'Duration cannot be 0.'})

            startTime = create_registration_form.cleaned_data['startTime']
            duration = datetime.timedelta(days=days, hours=hours, minutes=minutes)
            endTime = startTime + duration
            registration = Registration.objects.create(name=create_registration_form.cleaned_data['name'],
                                                       startTime=startTime,
                                                       duration=duration,
                                                       endTime=endTime)

            registration.save()
            return redirect('registration')

        return render(request, self.template_name, {'create_registration_form' : create_registration_form})

class RegistrationsView(View):
    """
    View for everyone to view all the registrations.
    """

    template_name = 'academicInfo/registration.html'

    def get(self, request, *args, **kwargs):

        time = timezone.now()

        future_registrations = Registration.objects.filter(startTime__gt=time).order_by('startTime')
        present_registrations = Registration.objects.filter(
                                                            endTime__gt=time
                                                            ).exclude(startTime__gt=time).order_by('endTime')
        past_registrations = Registration.objects.filter(endTime__lt=time)

        return render(request, self.template_name, {'future_registrations': future_registrations,
                                                    'present_registrations': present_registrations,
                                                    'past_registrations': past_registrations})

class LiveRegistrationView(LoginRequiredMixin, View):
    """
    View for student to register and unregister from live registrations.
    """

    template_name = 'academicInfo/live_registration.html'

    def get(self, request, *args, **kwargs):

        # Render this page only for the students.
        if hasattr(request.user, 'student'):

            registration = get_object_or_404(Registration, pk=self.kwargs['registration_id'])
            time = timezone.now()

            # Check if registration is currently live.
            if registration.startTime < time and registration.endTime > time:

                student = request.user.student

                # Show courses which are in either current semester or the next semester of student.
                courses_in_registration = registration.courseregistration_set.all()
                course_registration = courses_in_registration.filter(
                                                                     semester__gt=student.get_student_semester
                                                                     ).exclude(semester__gt=student.get_student_semester+1)
                return render(request, self.template_name, {'course_registration' : course_registration,
                                                            'student_courses' : student.courseregistration_set.all()})
            else:
                return redirect('registration')

        else:
            return redirect('home')

    def post(self, request, *args, **kwargs):

        # Only students should be allowed to register.
        if hasattr(request.user, 'student'):

            course_registration = get_object_or_404(CourseRegistration,
                                                    pk=request.POST['course_registration_id'])
            registration = course_registration.registration
            currTime = timezone.now()
            student = request.user.student
            semester = student.get_student_semester

            # If student wants to register for the course.
            if 'Register' in request.POST:
                if (currTime > registration.startTime and
                    currTime < registration.endTime and
                    course_registration.semester in range(semester, semester+2)):

                    if (not student in course_registration.students.all() and
                        course_registration.remaining_seats > 0):
                        course_registration.students.add(student)

                    return redirect(reverse('live_registration',
                                                kwargs={'registration_id' : registration.id}))

                else:
                    return redirect('home')

            # If student wants to unregister from the course.
            elif 'UnRegister' in request.POST:
                if (currTime > registration.startTime and
                    currTime < registration.endTime and
                    student in course_registration.students.all()):
                    course_registration.students.remove(student)

                return redirect(reverse('live_registration',
                                        kwargs={'registration_id' : registration.id}))

        else:
            return redirect('home')

class DepartmentsView(LoginRequiredMixin, View):
    """
    View for admin to see departments and add new department.
    """

    template_name = 'academicInfo/departments.html'

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            departments = Department.objects.all()
            return render(request, self.template_name, {'departments' : departments})
        else:
            return redirect('home')


class CourseView(LoginRequiredMixin, View):
    """
    View for admin to see Courses and add new Course.
    """

    template_name = 'academicInfo/courses.html'

    def get(self, request, *args, **kwargs):

        # Render this page only for the Admin.
        if hasattr(request.user, 'staff') and request.user.staff.is_admin:
            courses = Course.objects.all()
            return render(request, self.template_name, {'courses' : courses})
        else:
            return redirect('home')
