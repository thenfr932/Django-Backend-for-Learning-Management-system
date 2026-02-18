from rest_framework import serializers
from .models import Course, Module, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "module",
            "title",
            "content",
            "video_url",
            "duration_seconds",
            "is_preview",
            "order",
        ]


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "title", "description", "order", "lessons"]


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "owner",
            "title",
            "slug",
            "short_description",
            "long_description",
            "price",
            "status",
            "modules",
        ]
