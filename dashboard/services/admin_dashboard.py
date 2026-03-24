# dashboard/services/admin_dashboard.py

from django.db.models import Count
from django.contrib.auth import get_user_model

from courses.models import Course
from assignments.models import Submission

User = get_user_model()


class AdminDashboardService:
    def get_metrics(self):
        return {
            "total_users": User.objects.count(),
            "total_courses": Course.objects.count(),
            "total_submissions": Submission.objects.count(),
            "active_students": User.objects.filter(role="student").count(),
        }
