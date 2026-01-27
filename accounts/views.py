from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    ProfileSerializer,
    GoogleOAuthSerializer,
)
from rest_framework_simplejwt.exceptions import TokenError
from .models import Profile


class GoogleOAuthView(APIView):
    """
    Handle Google OAuth login/signup
    Expects a Google ID token from the frontend
    """

    def post(self, request):
        serializer = GoogleOAuthSerializer(data=request.data)
        # print(request.data)

        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create or get user
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Get oauth_profile_url URL
        oauth_profile_url = None
        if hasattr(user, "profile"):
            oauth_profile_url = user.profile.get_profile_url()

        response = Response(
            {
                "success": True,
                "message": "Google authentication successful",
                "userId": str(user.id),
                "username": user.username,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "oauth_profile_url": (
                    user.profile.oauth_profile_url if hasattr(user, "profile") else None
                ),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )

        # Set refresh token in httpOnly cookie
        response.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,
            samesite="Lax",
            secure=False,  # Set to True in production (HTTPS)
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        return response


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Auto-login after signup
        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "sucess": True,
                "message": "User created successfully",
                "username": user.username,
                "email": user.email,
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,
        )

        return response


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "success": True,
                "userId": user.id,
                "username": user.username,
                "email": user.email,
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
        # refreshtoken cookie
        response.set_cookie(
            key="refreshToken",
            value=str(refresh),
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=60 * 60 * 24 * 7,
        )

        return response


class RefreshView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refreshToken")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            token = RefreshToken(refresh_token)
            # Optionally rotate refresh token for better security
            token.set_jti()
            token.set_exp()
        except TokenError:
            return Response(
                {"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "success": True,
                "access": str(token.access_token),
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refreshToken")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Requires 'rest_framework_simplejwt.token_blacklist'
            except TokenError:
                pass

        response = Response({"success": True}, status=status.HTTP_200_OK)
        response.delete_cookie("refreshToken")
        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        serializer = ProfileSerializer(
            profile, data=request.data, partial=True  # allows partial updates
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
