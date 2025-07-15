from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

FIELD_TYPES = [
    ('text', 'Text'),
    ('number', 'Number'),
    ('date', 'Date'),
    ('password', 'Password'),
]

class DynamicForm(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DynamicField(models.Model):
    form = models.ForeignKey(DynamicForm, on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=255)
    field_type = models.CharField(choices=FIELD_TYPES, max_length=20)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.label} ({self.field_type})"

class Employee(models.Model):
    form = models.ForeignKey(DynamicForm, on_delete=models.SET_NULL, null=True)
    data = models.JSONField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
