from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login-register/', LoginRegisteredView),
    path('changepassword/', ChangePassword),
    path('register/', RegisterView.as_view()),
    path('login/', MyTokenView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]