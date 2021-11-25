from django.urls import path, include
from . import views

urlpatterns = [
    path('createCourse/', views.CreateCourseView.as_view(), name='create_course'),
    path('createCourseRegistration/', views.CreateCourseRegistrationView.as_view(), name='create_course_registration'),
    path('createRegistration/', views.CreateRegistrationView.as_view(), name='create_registration'),
    path('registration/', views.RegistrationsView.as_view(), name='registration'),
    path('<int:registration_id>', views.LiveRegistrationView.as_view(), name='live_registration'),
]
