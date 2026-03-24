# dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import IsTrainer, IsStudent, IsAdminUserRole
from .services.trainer_dashboard import TrainerDashboardService
from .services.student_dashboard import StudentDashboardService
from .services.admin_dashboard import AdminDashboardService
from .serializers import SubmissionSerializer, CourseSerializer, StudentSerializer


# ================= TRAINER =================
class TrainerDashboardView(APIView):
    permission_classes = [IsTrainer]

    def get(self, request):
        service = TrainerDashboardService(request.user)

        metrics = service.get_metrics()
        submissions = service.get_upcoming_assignments()
        my_courses = service.get_my_courses()
        my_students = service.get_my_students()
        print("helloo", my_students)

        return Response(
            {
                "metrics": metrics,
                "pending_reviews": SubmissionSerializer(submissions, many=True).data,
                "my_courses": CourseSerializer(my_courses, many=True).data,
                "my_students": StudentSerializer(my_students, many=True).data,
            }
        )


# ================= STUDENT =================
class StudentDashboardView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        service = StudentDashboardService(request.user)

        metrics = service.get_metrics()
        submissions = service.get_recent_submissions()

        return Response(
            {
                "metrics": metrics,
                "recent_submissions": SubmissionSerializer(submissions, many=True).data,
            }
        )


# ================= ADMIN =================
class AdminDashboardView(APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        service = AdminDashboardService()

        return Response({"metrics": service.get_metrics()})
