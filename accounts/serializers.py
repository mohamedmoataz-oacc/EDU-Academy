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