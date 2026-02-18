import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Course(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
        ("unlisted", "Unlisted"),
    ]

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # duration = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="public"
    )
    thumbnail_url = models.URLField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["owner"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
