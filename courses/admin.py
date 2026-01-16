from django.contrib import admin
from .models import Course, Lesson ,Module

# This tells Django to show these models in the admin panel
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)