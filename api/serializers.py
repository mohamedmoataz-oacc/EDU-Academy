from rest_framework import serializers
from .models import User, Teacher, Student, Assistant, Course

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'governorate', 'phone_number', 'gender', "user_role")

class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('personal_photo', 'national_ID_photo')

class AssistantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = ('birth_date', 'personal_photo', 'national_ID_photo')

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('birth_date', 'academic_year', 'study_field', 'parent_name',
                  'parent_phone_number', 'personal_photo'
            )

class CourseCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('subject', 'course_name', 'description', 'lecture_price',
                  'package_size', 'thumbnail'
        )
