from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginRegisteredView),
    path('change-password/', ChangePassword),
    path('register/', RegisterView.as_view()),
    path('login/', MyTokenView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
]