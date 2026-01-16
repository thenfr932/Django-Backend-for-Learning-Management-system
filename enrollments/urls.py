from django.urls import path
from .views import EnrollCourseView , EnrolledCourse

urlpatterns = [
    path("enroll/<slug:course_slug>/", EnrollCourseView.as_view()),
    path("my-enrollments/", EnrolledCourse.as_view()),
]
