from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import *
from .serializers import *

# Create your views here.
def FormBuilder(request):
    return render(request,"formbuilder.html")

def EmployeeList(request):
    return render(request,"employeelist.html")

class DynamicFormListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DynamicFormSerializer

    def get_queryset(self):
        return DynamicForm.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class DynamicFormDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = DynamicForm.objects.all()
    serializer_class = DynamicFormSerializer

class EmployeeListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmployeeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['data']

    def get_queryset(self):
        return Employee.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer