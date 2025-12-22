from django.urls import path
from .views import LoginView
from .views import RegisterView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
]
