from django.urls import path

from . import views

"""
URL patterns for the academicInfo application.
"""
urlpatterns = [
    path('createCourse/', views.CreateCourseView.as_view(), name='create_course'),
    path('viewCourse/', views.CourseView.as_view(), name='view_course'),
    path('createCourseRegistration/', views.CreateCourseRegistrationView.as_view(), name='create_course_registration'),
    path('createDepartment/', views.CreateDepartmentView.as_view(), name='create_department'),
    path('viewDepartment/', views.DepartmentsView.as_view(), name='view_department'),
    path('createRegistration/', views.CreateRegistrationView.as_view(), name='create_registration'),
    path('registration/', views.RegistrationsView.as_view(), name='registration'),
    path('live_registration/<int:registration_id>', views.LiveRegistrationView.as_view(), name='live_registration'),
]
