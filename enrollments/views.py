from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Enrollment, Progress
from .serializers import EnrollmentSerializer
from courses.models import Course, Lesson


class EnrollCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_slug):
        # print(f"Received EnrollCourseView HIT. Searching for: '{course_slug}'")
        user = request.user

        # Validate course
        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            return Response(
                {"detail": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        #  Create enrollment (idempotent)
        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                "role": "student",
                "status": "active"
            }
        )

        if not created:
            return Response(
                {"detail": "User already enrolled"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #  Initialize progress safely
        lessons = Lesson.objects.filter(course=course)

        Progress.objects.bulk_create(
            [
                Progress(
                    user=user,
                    course=course,
                    lesson=lesson
                )
                for lesson in lessons
            ],
            ignore_conflicts=True  #prevents duplicates
        )

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
