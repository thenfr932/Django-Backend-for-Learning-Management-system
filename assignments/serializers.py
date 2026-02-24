from rest_framework import serializers
from .models import (
    Assignment,
    QuizQuestion,
    QuizOption,
    Submission,
    SubmissionAnswer,
    ProjectFile,
)


class QuizOptionStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ["id", "option_text"]


class QuizQuestionStudentSerializer(serializers.ModelSerializer):
    options = QuizOptionStudentSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = ["id", "question_text", "question_type", "marks", "order", "options"]


class AssignmentStudentSerializer(serializers.ModelSerializer):
    questions = QuizQuestionStudentSerializer(many=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "title",
            "description",
            "assignment_type",
            "total_marks",
            "passing_marks",
            "due_date",
            "questions",
        ]


class SubmissionAnswerCreateSerializer(serializers.ModelSerializer):
    selected_options = serializers.PrimaryKeyRelatedField(
        many=True, queryset=QuizOption.objects.all(), required=False
    )

    class Meta:
        model = SubmissionAnswer
        fields = ["question", "selected_options", "text_answer"]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    answers = SubmissionAnswerCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Submission
        fields = ["assignment", "answers"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        student = self.context["request"].user

        submission = Submission.objects.create(student=student, **validated_data)

        total_marks = 0

        for answer_data in answers_data:
            selected_options = answer_data.pop("selected_options", [])
            question = answer_data["question"]

            answer = SubmissionAnswer.objects.create(
                submission=submission,
                question=question,
                text_answer=answer_data.get("text_answer", ""),
            )

            answer.selected_options.set(selected_options)

            # 🔥 Auto-grading for MCQ
            correct_options = question.options.filter(is_correct=True)
            if question.question_type.startswith("mcq"):
                if set(correct_options) == set(selected_options):
                    answer.is_correct = True
                    answer.marks_awarded = question.marks
                    total_marks += question.marks

            answer.save()

        submission.marks_obtained = total_marks
        submission.status = "graded"
        submission.save()

        return submission


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ["file"]


class ProjectSubmissionSerializer(serializers.ModelSerializer):
    files = ProjectFileSerializer(many=True, write_only=True)

    class Meta:
        model = Submission
        fields = ["assignment", "files"]

    def create(self, validated_data):
        files_data = validated_data.pop("files")
        student = self.context["request"].user

        submission = Submission.objects.create(student=student, **validated_data)

        for file_data in files_data:
            ProjectFile.objects.create(submission=submission, file=file_data["file"])

        return submission


class SubmissionStudentViewSerializer(serializers.ModelSerializer):
    answers = SubmissionAnswerCreateSerializer(many=True)
    files = ProjectFileSerializer(many=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "assignment",
            "marks_obtained",
            "feedback",
            "status",
            "submitted_at",
            "answers",
            "files",
        ]


# Faculty Serializers
class QuizOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ["option_text", "is_correct"]


class QuizQuestionCreateSerializer(serializers.ModelSerializer):
    options = QuizOptionCreateSerializer(many=True)

    class Meta:
        model = QuizQuestion
        fields = ["question_text", "question_type", "marks", "order", "options"]

    def create(self, validated_data):
        options_data = validated_data.pop("options")
        question = QuizQuestion.objects.create(**validated_data)

        for option_data in options_data:
            QuizOption.objects.create(question=question, **option_data)

        return question


class AssignmentCreateSerializer(serializers.ModelSerializer):
    questions = QuizQuestionCreateSerializer(many=True, required=False)

    class Meta:
        model = Assignment
        fields = [
            "course",
            "lesson",
            "title",
            "description",
            "assignment_type",
            "total_marks",
            "passing_marks",
            "due_date",
            "is_published",
            "questions",
        ]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        assignment = Assignment.objects.create(**validated_data)

        for question_data in questions_data:
            options_data = question_data.pop("options")
            question = QuizQuestion.objects.create(
                assignment=assignment, **question_data
            )
            for option_data in options_data:
                QuizOption.objects.create(question=question, **option_data)

        return assignment


class SubmissionFacultySerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    answers = SubmissionAnswerCreateSerializer(many=True)
    files = ProjectFileSerializer(many=True)

    class Meta:
        model = Submission
        fields = "__all__"
