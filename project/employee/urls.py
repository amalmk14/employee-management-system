from django.urls import path
from .views import *

urlpatterns = [
    path('formbuilder/',FormBuilder),
    path('employeelist/',EmployeeList),
    path('forms/', DynamicFormListCreate.as_view()),
    path('forms/<int:pk>/', DynamicFormDetail.as_view()),
    path('employees/', EmployeeListCreate.as_view()),
    path('employees/<int:pk>/', EmployeeDetail.as_view()),
]