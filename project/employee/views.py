from django.shortcuts import render
from rest_framework import generics, permissions, filters
from .models import *
from .serializers import *

# Create your views here.
def FormPage(request):
    return render(request,"form.html")

def EmployeeList(request):
    return render(request,"employeelist.html")

from rest_framework.response import Response
from rest_framework import status


class FormListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FormSerializer

    def get_queryset(self):
        return Form.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class FormDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Form.objects.all()
    serializer_class = FormSerializer

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