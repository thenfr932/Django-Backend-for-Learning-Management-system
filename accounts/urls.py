from django.urls import path
from .views import (
    LoginView,
    ProfileView,
    RegisterView,
    LogoutView,
    RefreshView,
    GoogleOAuthView,
)

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("refresh/", RefreshView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("google/", GoogleOAuthView.as_view()),
]
