import uuid
from django.db import models
from django.conf import settings


# ==========================
# ASSIGNMENT (PARENT MODEL)
# ==========================


class Assignment(models.Model):
    TYPE_CHOICES = [
        ("quiz", "Quiz"),
        ("project", "Project Upload"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    course = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, related_name="assignments"
    )

    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assignments",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    assignment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    total_marks = models.PositiveIntegerField(default=0)
    passing_marks = models.PositiveIntegerField(default=0)

    due_date = models.DateTimeField(null=True, blank=True)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.assignment_type})"


# ==========================
# QUIZ QUESTIONS
# ==========================


class QuizQuestion(models.Model):
    QUESTION_TYPE = [
        ("mcq_single", "MCQ - Single Correct"),
        ("mcq_multiple", "MCQ - Multiple Correct"),
        ("text", "Short Text Answer"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="questions"
    )

    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE)
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question_text[:50]


class QuizOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    question = models.ForeignKey(
        QuizQuestion, on_delete=models.CASCADE, related_name="options"
    )

    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text


# ==========================
# STUDENT SUBMISSION
# ==========================


class Submission(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("graded", "Graded"),
        ("late", "Late"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    marks_obtained = models.FloatField(default=0)
    feedback = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="submitted"
    )

    class Meta:
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student.email} - {self.assignment.title}"


# ==========================
# QUIZ ANSWERS (FOR QUIZ TYPE)
# ==========================


class SubmissionAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="answers"
    )

    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)

    selected_options = models.ManyToManyField(QuizOption, blank=True)

    text_answer = models.TextField(blank=True)

    is_correct = models.BooleanField(default=False)
    marks_awarded = models.FloatField(default=0)

    def __str__(self):
        return f"Answer for {self.question.question_text[:30]}"


# ==========================
# PROJECT FILE UPLOAD
# ==========================


class ProjectFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, related_name="files"
    )

    file = models.FileField(upload_to="assignments/projects/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
