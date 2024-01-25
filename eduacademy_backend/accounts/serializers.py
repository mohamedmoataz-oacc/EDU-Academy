from rest_framework import serializers
from .models import *

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
    
    def save(self, request):
        data = self.data
        return User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            governorate=data['governorate'],
            phone_number=data['phone_number'],
            gender=data['gender'],
            birth_date = data['birth_date'],
            user_role=UsersRole.objects.get(pk=data['user_role']),
        )