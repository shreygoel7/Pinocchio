from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('studentSignup/', views.StudentSignUp.as_view(), name='student_sign_up'),
    path('facultySignup/', views.FacultySignUp.as_view(), name='faculty_sign_up'),
    path('staffSignup/', views.StaffSignUp.as_view(), name='staff_sign_up'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
]
