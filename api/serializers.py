from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_username(self, value): return value

class SignupSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(max_length=15)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'governorate', 'phone_number', 'gender', 'birth_date', 'user_role')
    
    def validate_user_role(self, value):
        role = UsersRole.objects.filter(role=value)
        if len(role) == 0:
            raise serializers.ValidationError("There is no such role.")
        return role[0].pk

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

class CourseCreationSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(max_length=50)
    class Meta:
        model = Course
        fields = ('subject', 'course_name', 'description', 'lecture_price',
                  'package_size', 'thumbnail'
        )

    def validate_subject(self, value):
        subject = Subject.objects.filter(subject_name=value)
        if len(subject) == 0:
            raise serializers.ValidationError("There is no such subject.")
        return subject[0].pk
    
class LectureCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ('lecture_title','video')