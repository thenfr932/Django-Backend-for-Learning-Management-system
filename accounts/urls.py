from django.urls import path
from .views import LoginView
from .views import RegisterView
from .views import ProfileUpdateView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("profile/",ProfileUpdateView.as_view()),
]
