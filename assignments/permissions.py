from rest_framework.permissions import BasePermission
from enrollments.models import Enrollment


class IsFaculty(BasePermission):
    """
    Allows access only to instructors (course owner).
    """

    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user


class IsEnrolledStudent(BasePermission):
    """
    Allows access only to students enrolled in the course.
    """

    def has_object_permission(self, request, view, obj):
        return Enrollment.objects.filter(
            user=request.user, course=obj.course, role="student", status="active"
        ).exists()
