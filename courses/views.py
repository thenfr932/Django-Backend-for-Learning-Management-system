from rest_framework.permissions import IsAuthenticated
from .serializers import CourseSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from rest_framework.views import APIView


# Create your views here.
class AllCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_slug):
        user = request.user

        course = Course.objects.get(slug=course_slug)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
