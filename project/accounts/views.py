from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, ProfileSerializer, MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

User = get_user_model()


def LoginRegisteredView(request):
    return render(request, 'login.html')

def ChangePassword(request):
    return render(request, 'change-password.html')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Wrong old password."}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"success": "Password changed successfully."})

class MyTokenView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer