from django.urls import path
from .views import *

urlpatterns = [
    path('form/',FormPage),
    path('employeelist/',EmployeeList),
    path('forms/', FormListCreate.as_view()),
    path('forms/<int:pk>/', FormDetail.as_view()),
    path('employees/', EmployeeListCreate.as_view()),
    path('employees/<int:pk>/', EmployeeDetail.as_view()),
]