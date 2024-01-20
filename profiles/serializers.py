from rest_framework import serializers
from accounts.models import *

class UserRoleSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(max_length=15)
    class Meta:
        model = User
        fields = ('user_role',)
    
    def validate_user_role(self, value):
        role = UsersRole.objects.filter(role=value)
        if not role.exists():
            raise serializers.ValidationError("There is no such role.")
        return role[0].pk

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('governorate', 'phone_number')

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
