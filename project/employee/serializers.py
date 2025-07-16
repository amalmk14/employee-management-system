from rest_framework import serializers
from .models import *


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        exclude = ['form'] 

class FormSerializer(serializers.ModelSerializer):
    fields = FormFieldSerializer(many=True)

    class Meta:
        model = Form
        fields = ['id', 'name', 'created_at', 'fields']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['fields'] = FormFieldSerializer(instance.fields.all(), many=True).data
        return rep

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        form = Form.objects.create(**validated_data)  
        for field in fields_data:
            FormField.objects.create(form=form, **field)
        return form

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        instance.fields.all().delete()
        for field in fields_data:
            FormField.objects.create(form=instance, **field)
        return instance



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['created_by']
