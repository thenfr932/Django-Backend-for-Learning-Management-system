# dashboard/services/student_dashboard.py

from django.db.models import Count, Avg
from django.utils import timezone

from enrollments.models import Enrollment
from assignments.models import Submission


class StudentDashboardService:
    def __init__(self, user):
        self.user = user

    def get_metrics(self):
        enrolled_courses = Enrollment.objects.filter(
            user=self.user, role="student", status="active"
        )

        submissions = Submission.objects.filter(student=self.user)

        completed_assignments = submissions.filter(status="graded").count()

        avg_marks = submissions.aggregate(avg=Avg("marks_obtained"))["avg"] or 0

        return {
            "enrolled_courses": enrolled_courses.count(),
            "completed_assignments": completed_assignments,
            "average_marks": round(avg_marks, 2),
        }

    def get_recent_submissions(self):
        return (
            Submission.objects.filter(student=self.user)
            .select_related("assignment", "assignment__course")
            .order_by("-submitted_at")[:5]
        )
