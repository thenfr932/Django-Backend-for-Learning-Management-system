# dashboard/urls.py

from django.urls import path
from .views import (
    TrainerDashboardView,
    StudentDashboardView,
    AdminDashboardView,
)

urlpatterns = [
    path("trainer/", TrainerDashboardView.as_view(), name="trainer-dashboard"),
    path("student/", StudentDashboardView.as_view(), name="student-dashboard"),
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
]
