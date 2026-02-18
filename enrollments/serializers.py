from rest_framework import serializers
from .models import Enrollment, Progress


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "role", "status", "enrolled_at"]
        read_only_fields = ["id", "course", "role", "status", "enrolled_at"]


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [
            "id",
            "user",
            "course",
            "lesson",
            "watched_seconds",
            "completed",
            "last_seen_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "course",
            "lesson",
            "watched_seconds",
            "completed",
            "last_seen_at",
        ]
