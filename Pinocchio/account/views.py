from faculty.forms import FacultySignupForm
from faculty.models import Faculty

from staff.forms import StaffSignupForm
from staff.models import Staff

from student.forms import StudentSignupForm
from student.models import Student

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from .forms import LoginForm
# Create your views here.

class FacultySignUp(View):
    template_name = 'account/faculty_signup.html'
    faculty_signup_form = FacultySignupForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            faculty_signup_form = self.faculty_signup_form()
            return render(request, self.template_name, {'faculty_signup_form' : faculty_signup_form})

    def post(self, request, *args, **kwargs):
        faculty_signup_form = FacultySignupForm(request.POST)
        if faculty_signup_form.is_valid():
            user = faculty_signup_form.save()
            user.save()
            faculty = Faculty(user=user, dob=faculty_signup_form.cleaned_data['dob'],
                              department=faculty_signup_form.cleaned_data['department'])
            faculty.save()
            auth.login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'faculty_signup_form' : faculty_signup_form})

class StaffSignUp(View):
    template_name = 'account/staff_signup.html'
    staff_signup_form = StaffSignupForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            staff_signup_form = self.staff_signup_form()
            return render(request, self.template_name, {'staff_signup_form' : staff_signup_form})

    def post(self, request, *args, **kwargs):
        staff_signup_form = StaffSignupForm(request.POST)
        if staff_signup_form.is_valid():
            user = staff_signup_form.save()
            user.save()
            staff = Staff(user=user, dob=staff_signup_form.cleaned_data['dob'])
            staff.save()
            auth.login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'staff_signup_form' : staff_signup_form})

class StudentSignUp(View):
    template_name = 'account/student_signup.html'
    student_signup_form = StudentSignupForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            student_signup_form = self.student_signup_form()
            return render(request, self.template_name, {'student_signup_form' : student_signup_form})

    def post(self, request, *args, **kwargs):
        student_signup_form = StudentSignupForm(request.POST)
        if student_signup_form.is_valid():
            user = student_signup_form.save()
            user.save()
            student = Student(user=user, dob=student_signup_form.cleaned_data['dob'],
                              batch=student_signup_form.cleaned_data['batch'],
                              department=student_signup_form.cleaned_data['department'])
            student.save()
            auth.login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'student_signup_form' : student_signup_form})

class UserProfile(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'student'):
            student = request.user.student
            return render(request, self.template_name, {'user' : request.user, 'courses' : student.courseregistration_set.all() })

        else:
            return redirect('home')

class LoginView(View):
    template_name = 'account/login.html'
    login_form = LoginForm

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_form = self.login_form()
            return render(request, self.template_name, {'login_form': login_form})

        return redirect('home')

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        
        if login_form.is_valid():
            user = authenticate(username=login_form.cleaned_data['username'],
                                password=login_form.cleaned_data['password'])

            if user is not None:
                auth.login(request, user)
                if 'next' in request.GET:
                    return redirect(request.GET['next'])
                return redirect('home')

            login_form.add_error('username', 'Incorrect username or password')
            login_form.add_error('password', 'Incorrect username or password')
            return render(request, self.template_name, {'login_form':login_form})

        return render(request, self.template_name, {'login_form':login_form})

class LogoutView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('home')
