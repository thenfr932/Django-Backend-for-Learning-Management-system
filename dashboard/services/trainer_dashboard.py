# dashboard/services/trainer_dashboard.py

from django.db.models import Count, Avg, Q
from django.utils import timezone

from courses.models import Course
from enrollments.models import Enrollment
from assignments.models import Submission


class TrainerDashboardService:
    def __init__(self, user):
        self.user = user

    def get_metrics(self):
        courses = Course.objects.filter(owner=self.user)

        total_students = Enrollment.objects.filter(
            course__owner=self.user, role="student", status="active"
        ).count()

        pending_reviews = Submission.objects.filter(
            assignment__course__owner=self.user,
            status="submitted",
        ).count()

        # avg_rating = 4.8  # Placeholder (no rating model provided)

        return {
            "my_courses": courses.count(),
            "total_students": total_students,
            "pending_reviews": pending_reviews,
            # "avg_rating": avg_rating,
        }

    def get_upcoming_assignments(self):
        return (
            Submission.objects.filter(
                assignment__course__owner=self.user,
                status="submitted",
            )
            .select_related("assignment", "student")
            .order_by("submitted_at")[:5]
        )

    def get_my_courses(self):
        return Course.objects.filter(owner=self.user)

    def get_my_students(self):
        # print(Enrollment.objects.filter(course__owner=self.user, role="student"))
        return Enrollment.objects.filter(course__owner=self.user, role="student")
