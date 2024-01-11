from rest_framework import serializers
from accounts.models import *

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('personal_photo', 'national_ID_photo')

class AssistantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ('personal_photo', 'national_ID_photo')

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('academic_year', 'study_field', 'parent_name', 'parent_phone_number', 'personal_photo')
