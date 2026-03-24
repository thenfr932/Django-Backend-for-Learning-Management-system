# dashboard/serializers.py

from rest_framework import serializers
from assignments.models import Submission
from courses.models import Course
from enrollments.models import Enrollment
from accounts.models import User


class SubmissionSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source="assignment.title")
    student_email = serializers.CharField(source="student.email")

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment_title",
            "student_email",
            "marks_obtained",
            "status",
            "submitted_at",
        ]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "slug", "status"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
