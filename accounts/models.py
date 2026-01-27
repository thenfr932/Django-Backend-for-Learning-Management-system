import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    google_id = models.CharField(
        max_length=255, blank=True, unique=True, null=True, db_index=True
    )

    auth_provider = models.CharField(
        max_length=255,
        choices=[("google", "Google OAuth"), ("email", "Email/Password")],
        default="email",
    )

    is_oauth_user = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["google_id"]),
        ]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    job_title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    oauth_profile_url = models.URLField(
        blank=True, help_text="URL to the user's profile on the OAuth provider"
    )
    linkedin_url = models.URLField(blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=64, default="UTC")
    locale = models.CharField(max_length=32, default="en")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile({self.user.email})"

    def get_profile_url(self):
        return self.oauth_profile_url or None
