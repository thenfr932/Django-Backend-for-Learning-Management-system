from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import User, Profile
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.db import transaction


class GoogleOAuthSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, token):
        """Validate Google ID token"""
        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID
            )

            # Verify the token is for your app
            if idinfo["aud"] != settings.GOOGLE_OAUTH_CLIENT_ID:
                raise serializers.ValidationError("Invalid token audience")

            # Token is valid, return user info
            return idinfo

        except ValueError as e:
            raise serializers.ValidationError(f"Invalid token: {str(e)}")

    @transaction.atomic
    def create(self, validated_data):
        """Create or get user from Google data"""
        google_data = validated_data["token"]

        email = google_data.get("email")
        google_id = google_data.get("sub")
        first_name = google_data.get("given_name", "")
        last_name = google_data.get("family_name", "")
        picture = google_data.get("picture", "")

        # Check if user exists by google_id first
        user = User.objects.filter(google_id=google_id).first()

        if user:
            # Update user info if needed
            if user.first_name != first_name or user.last_name != last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            # Update profile picture if changed
            if hasattr(user, "profile") and user.profile.oauth_profile_url != picture:
                user.profile.oauth_profile_url = picture
                user.profile.save()

            return user

        # Check if user exists by email (for account linking)
        user = User.objects.filter(email=email).first()

        if user:
            # Link Google account to existing user
            user.google_id = google_id
            user.auth_provider = "google"
            user.is_oauth_user = True
            if not user.first_name:
                user.first_name = first_name
            if not user.last_name:
                user.last_name = last_name
            user.save()

            # Update or create profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.oauth_profile_url = picture
            profile.save()

            return user

        # Create new user
        # Generate unique username from email
        base_username = email.split("@")[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            google_id=google_id,
            auth_provider="google",
            is_oauth_user=True,
        )

        # No password for OAuth users
        user.set_unusable_password()
        user.save()

        # Create profile with Google picture
        # Profile.objects.create(
        #     user=user,
        #     oauth_profile_url=picture,
        # )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        newuser = get_user_model().objects.create_user(**validated_data)
        return newuser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "job_title",
            "bio",
            "company",
            "oauth_profile_url",
            "linkedin_url",
            "preferences",
            "timezone",
            # "locale",
        ]
