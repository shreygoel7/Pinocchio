from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('account/', include('account.urls')),
    path('academicInfo/', include('academicInfo.urls')),
]
