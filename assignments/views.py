from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import QuerySet

from .models import Assignment, Submission
from .serializers import (
    AssignmentStudentSerializer,
    AssignmentCreateSerializer,
    SubmissionCreateSerializer,
    ProjectSubmissionSerializer,
    SubmissionStudentViewSerializer,
    SubmissionFacultySerializer,
)
from .permissions import IsFaculty, IsEnrolledStudent
from enrollments.models import Enrollment


# Student ViewSets
# class AssignmentStudentViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Students can view published assignments.
#     """

#     serializer_class = AssignmentStudentSerializer
#     permission_classes = [IsAuthenticated, IsStudent]

#     def get_queryset(self) -> QuerySet:
#         return Assignment.objects.filter(is_published=True)


# class QuizSubmissionViewSet(viewsets.ModelViewSet):
#     """
#     Students submit quiz-type assignments.
#     """

#     serializer_class = SubmissionCreateSerializer
#     permission_classes = [IsAuthenticated, IsStudent]

#     def get_queryset(self) -> QuerySet:
#         return Submission.objects.filter(student=self.request.user)


# class ProjectSubmissionViewSet(viewsets.ModelViewSet):
#     """
#     Students submit project-type assignments.
#     """

#     serializer_class = ProjectSubmissionSerializer
#     permission_classes = [IsAuthenticated, IsStudent]

#     def get_queryset(self) -> QuerySet:
#         return Submission.objects.filter(student=self.request.user)


# class StudentSubmissionViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = SubmissionStudentViewSerializer
#     permission_classes = [IsAuthenticated, IsStudent, IsSubmissionOwner]

#     def get_queryset(self) -> QuerySet:
#         return Submission.objects.filter(student=self.request.user)


class StudentAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Only courses where student is enrolled
        enrolled_courses = Enrollment.objects.filter(
            user=user, role="student", status="active"
        ).values_list("course_id", flat=True)

        return Assignment.objects.filter(
            course_id__in=enrolled_courses, is_published=True
        )

    def retrieve(self, request, *args, **kwargs):
        assignment = self.get_object()

        # Extra safety check
        if not Enrollment.objects.filter(
            user=request.user, course=assignment.course, role="student", status="active"
        ).exists():
            return Response({"detail": "Not enrolled."}, status=403)

        serializer = self.get_serializer(assignment)
        return Response(serializer.data)


class StudentSubmissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Submission.objects.filter(student=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            assignment_type = self.request.data.get("assignment_type")

            if assignment_type == "quiz":
                return SubmissionCreateSerializer
            elif assignment_type == "project":
                return ProjectSubmissionSerializer

        return SubmissionStudentViewSerializer

    def create(self, request, *args, **kwargs):
        assignment_id = request.data.get("assignment")

        try:
            assignment = Assignment.objects.get(id=assignment_id, is_published=True)
        except Assignment.DoesNotExist:
            return Response({"detail": "Assignment not found."}, status=404)

        # Check enrollment
        if not Enrollment.objects.filter(
            user=request.user, course=assignment.course, role="student", status="active"
        ).exists():
            return Response({"detail": "Not enrolled."}, status=403)

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


# Faculty ViewSets


# class AssignmentFacultyViewSet(viewsets.ModelViewSet):
#     """
#     Faculty can create/update/delete assignments.
#     """

#     serializer_class = AssignmentCreateSerializer
#     permission_classes = [IsAuthenticated, IsFaculty]

#     def get_queryset(self) -> QuerySet:
#         return Assignment.objects.all()


# class SubmissionFacultyViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Faculty can view all submissions.
#     """

#     serializer_class = SubmissionFacultySerializer
#     permission_classes = [IsAuthenticated, IsFaculty]


#     def get_queryset(self) -> QuerySet:
#         return Submission.objects.all()
class FacultyAssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentCreateSerializer
    permission_classes = [IsAuthenticated, IsFaculty]

    def get_queryset(self) -> QuerySet[Assignment]:
        return Assignment.objects.filter(course__owner=self.request.user)

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]

        if course.owner != self.request.user:
            raise PermissionDenied("You are not the course owner.")

        serializer.save()

    @action(detail=True, methods=["get"])
    def submissions(self, request, pk=None):
        assignment = self.get_object()

        submissions = assignment.submissions.all()
        serializer = SubmissionFacultySerializer(submissions, many=True)
        return Response(serializer.data)
