from django.urls import path
from .views import EnrollCourseView, EnrolledCourse, ProgressView

urlpatterns = [
    path("enroll/<slug:course_slug>/", EnrollCourseView.as_view()),
    path("my-enrollments/", EnrolledCourse.as_view()),
    path("progress/<slug:course_slug>/<slug:lesson_slug>/", ProgressView.as_view()),
]
