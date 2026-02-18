from django.urls import path
from .views import AllCourseView, CourseView

urlpatterns = [
    path("get-all-courses/", AllCourseView.as_view()),
    path("course/<slug:course_slug>/", CourseView.as_view()),
]
