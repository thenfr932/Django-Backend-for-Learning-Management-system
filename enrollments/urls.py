from django.urls import path
from .views import EnrollCourseView

urlpatterns = [
    path("enroll/<slug:course_slug>/", EnrollCourseView.as_view()),
]
