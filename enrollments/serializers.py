from rest_framework import serializers
from .models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ["id", "user", "course", "role", "status", "enrolled_at"]
        read_only_fields = ["id","user","role","status", "enrolled_at"]
        