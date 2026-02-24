# from rest_framework.routers import DefaultRouter
# from .views import (
#     AssignmentStudentViewSet,
#     AssignmentFacultyViewSet,
#     QuizSubmissionViewSet,
#     ProjectSubmissionViewSet,
#     StudentSubmissionViewSet,
#     SubmissionFacultyViewSet,
# )

# router = DefaultRouter()

# # Student routes
# router.register(
#     r"student/assignments", AssignmentStudentViewSet, basename="student-assignments"
# )
# router.register(
#     r"student/quiz-submissions", QuizSubmissionViewSet, basename="quiz-submissions"
# )
# router.register(
#     r"student/project-submissions",
#     ProjectSubmissionViewSet,
#     basename="project-submissions",
# )
# router.register(
#     r"student/submissions", StudentSubmissionViewSet, basename="student-submissions"
# )

# # Faculty routes
# router.register(
#     r"faculty/assignments", AssignmentFacultyViewSet, basename="faculty-assignments"
# )
# router.register(
#     r"faculty/submissions", SubmissionFacultyViewSet, basename="faculty-submissions"
# )

# urlpatterns = router.urls
from rest_framework.routers import DefaultRouter
from .views import (
    StudentAssignmentViewSet,
    StudentSubmissionViewSet,
    FacultyAssignmentViewSet,
)

router = DefaultRouter()

router.register(
    r"student/assignments", StudentAssignmentViewSet, basename="student-assignments"
)
router.register(
    r"student/submissions", StudentSubmissionViewSet, basename="student-submissions"
)
router.register(
    r"faculty/assignments", FacultyAssignmentViewSet, basename="faculty-assignments"
)

urlpatterns = router.urls
