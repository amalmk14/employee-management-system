# employee-management-system


# Project: employee_mgmt (Single App Version) – Complete with Class-Based Views

# ---- FILE: core/models.py ----

from django.db import models
from django.contrib.auth.models import User

FIELD_TYPES = (
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('password', 'Password'),
)

class FormField(models.Model):
    label = models.CharField(max_length=100)
    field_type = models.CharField(choices=FIELD_TYPES, max_length=20)
    order = models.IntegerField(default=0)

class Employee(models.Model):
    form_data = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

# ---- FILE: core/serializers.py ----

from rest_framework import serializers
from .models import FormField, Employee
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

# ---- FILE: core/views.py ----

from rest_framework import generics, viewsets, permissions, status
from .models import FormField, Employee
from .serializers import (
    RegisterSerializer, FormFieldSerializer, EmployeeSerializer,
    ChangePasswordSerializer, ProfileSerializer
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"status": "Password updated successfully."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FormFieldViewSet(viewsets.ModelViewSet):
    queryset = FormField.objects.all().order_by('order')
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Employee.objects.filter(created_by=self.request.user)
        keyword = self.request.query_params.get('search')
        if keyword:
            queryset = [e for e in queryset if keyword.lower() in str(e.form_data).lower()]
        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# ---- FILE: core/urls.py ----

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, FormFieldViewSet, EmployeeViewSet, ChangePasswordView, ProfileView

router = DefaultRouter()
router.register(r'fields', FormFieldViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('', include(router.urls)),
]

# ---- FILE: templates/index.html ----

<!DOCTYPE html>
<html>
<head>
  <title>Employee Manager</title>
  <script>
    let token = '';

    async function login() {
      const res = await fetch('/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'adminpass' })
      });
      const data = await res.json();
      token = data.access;
      loadFields();
      listEmployees();
    }

    async function loadFields() {
      const res = await fetch('/api/fields/', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const fields = await res.json();
      const form = document.getElementById('dynForm');
      form.innerHTML = '';
      fields.forEach(field => {
        const input = document.createElement('input');
        input.name = field.label;
        input.type = field.field_type;
        input.placeholder = field.label;
        form.appendChild(input);
      });
    }

    async function submitEmployee() {
      const data = {};
      const form = document.getElementById('dynForm');
      for (const input of form.elements) {
        data[input.name] = input.value;
      }
      await fetch('/api/employees/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({ form_data: data })
      });
      listEmployees();
    }

    async function listEmployees() {
      const res = await fetch('/api/employees/', {
        headers: { 'Authorization': 'Bearer ' + token }
      });
      const employees = await res.json();
      const container = document.getElementById('empList');
      container.innerHTML = '';
      employees.forEach(emp => {
        const div = document.createElement('div');
        div.innerText = JSON.stringify(emp.form_data);
        const btn = document.createElement('button');
        btn.innerText = 'Delete';
        btn.onclick = () => deleteEmployee(emp.id);
        div.appendChild(btn);
        container.appendChild(div);
      });
    }

    async function deleteEmployee(id) {
      await fetch(`/api/employees/${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + token }
      });
      listEmployees();
    }
  </script>
</head>
<body onload="login()">
  <h2>Dynamic Employee Form</h2>
  <form id="dynForm"></form>
  <button onclick="submitEmployee()">Submit</button>
  <h3>Employee List</h3>
  <div id="empList"></div>
</body>
</html>
