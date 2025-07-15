from rest_framework import serializers
from .models import *

class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = '__all__'

class DynamicFormSerializer(serializers.ModelSerializer):
    fields = DynamicFieldSerializer(many=True, required=False)

    class Meta:
        model = DynamicForm
        fields = ['id', 'name', 'created_by', 'created_at', 'fields']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        form = DynamicForm.objects.create(**validated_data)
        for field_data in fields_data:
            DynamicField.objects.create(form=form, **field_data)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        instance.fields.all().delete()
        for field_data in fields_data:
            DynamicField.objects.create(form=instance, **field_data)

        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
