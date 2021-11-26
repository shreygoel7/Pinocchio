from django.contrib import admin
from .models import (Course,
                     CourseRegistration,
                     Department,
                     Registration)

# Register your models here.
admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(Department)
admin.site.register(Registration)
