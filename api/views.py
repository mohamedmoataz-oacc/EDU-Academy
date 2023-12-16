from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import bad_request
# return bad_request(request, "Either the username or email address is already associated with an account.")

from .models import *
from .views_checks import *
from .serializers import *

import base64

# Other functionalities:
# 1. See all courses and be able to filter by subject and grade
# 2. See all teachers and be able to filter by subject and grade
# 3. Get the student's points

###########
# Sign up #
###########

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect("api:complete_profile")
    
    if request.method == 'GET':
        required_data = {
            "required_data": [
                'username', 'email', 'password', 'first_name', 'last_name',
                'governerate', 'phone_number', 'gender', 'user_role',
            ],
        }
        return Response(required_data)
    elif request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            governorate=data['governorate'],
            phone_number=data['phone_number'],
            gender=data['gender'],
            user_role=UsersRole.objects.get(pk=data['user_role']),
        )
        return redirect("api:login")
        
##################
# Login & Logout #
##################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return redirect("api:complete_profile")
    
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     data = serializer.data()
        data = serializer.initial_data
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if profile_is_completed(user):
                return redirect("api:home")
            else: return redirect("api:complete_profile")
        else:
            return Response(data="The username or password is incorrect.", status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        required_data = {
            "required_data": ['username', 'password'],
        }
        return Response(required_data)
    
@login_required
@api_view(['GET'])
def logout_user(request):
    logout(request)
    return redirect("api:login")

######################
# Profile completion #
######################

@login_required
@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def complete_profile(request):
    if profile_is_completed(request.user):
        return redirect("api:home")
    
    roles_to_profiles = {
        "Teacher": teacher_complete_profile,
        "Student": student_complete_profile,
        "Assistant": assistant_complete_profile,
    }

    return roles_to_profiles[request.user.user_role.role](request)

# Note that `request.FILES` will only contain data if the request method was POST,
# at least one file field was actually posted,
# and the <form> that posted the request has the attribute enctype="multipart/form-data".
# Otherwise, `request.FILES` will be empty.

def teacher_complete_profile(request):
    if request.method == 'GET':
        required_data = [{
            "required_data": ['personal_photo', 'national_ID_photo'],
        }]
        return Response(required_data)
    elif request.method == 'POST':
        serializer = TeacherProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        
        Teacher(
            teacher=request.user,
            personal_photo = data['personal_photo'],
            national_ID_photo = data['national_ID_photo'],
        ).save()
        return redirect("api:view_profile", username=request.user.username)

def student_complete_profile(request):
    if request.method == 'GET':
        required_data = [{
            "required_data": ['birth_date', 'academic_year', 'study_field', 'parent_name',
                              'parent_phone_number', 'personal_photo'
                            ],
        }]
        return Response(required_data)
    elif request.method == 'POST':
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        
        Student(
            student=request.user,
            birth_date = data['birth_date'],
            academic_year = data['academic_year'],
            study_field = data['study_field'] if data.get('study_field') else None,
            parent_name = data['parent_name'],
            parent_phone_number = data['parent_phone_number'],
            personal_photo = data['personal_photo'] if data.get('personal_photo') else None,
        ).save()
        return redirect("api:view_profile", username=request.user.username)

def assistant_complete_profile(request):
    if request.method == 'GET':
        required_data = [{
            "required_data": ['birth_date', 'personal_photo', 'national_ID_photo'],
        }]
        return Response(required_data)
    elif request.method == 'POST':
        serializer = AssistantProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        
        Assistant(
            assistant=request.user,
            birth_date = data['birth_date'],
            personal_photo = data['personal_photo'],
            national_ID_photo = data['national_ID_photo'],
        ).save()
        return redirect("api:view_profile", username=request.user.username)

###################
# Profile viewing #
###################
    
@login_required
@api_view(['GET'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def view_profile(request, username=None):
    if username is None:
        return redirect("api:view_profile", username=request.user.username)
    user = get_object_or_404(User, username=username)

    roles_to_profiles = {
        "Teacher": teacher_view_profile,
        "Student": student_view_profile,
        "Assistant": assistant_view_profile
    }
    profile = {
        "view_self": request.user == user, # indicates whether the user searches for himself or another
        "username" : username,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "governorate" : user.governorate,
        "email" : user.email,
        "date_joined" : user.date_joined,
        "gender" : user.gender,
        "phone_number" : user.phone_number,
        "user_role" : user.user_role.role
    }
    return roles_to_profiles[user.user_role.role](user, profile)

def teacher_view_profile(user, user_profile: dict):
    teacher = Teacher.objects.get(teacher=user)
    photo_data = teacher.personal_photo.read() if teacher.personal_photo else None
    national_photo_data = teacher.national_ID_photo.read() if teacher.national_ID_photo else None
    user_profile.update(
        {
            "balance" : teacher.balance,
            "accepted" : teacher.accepted,
            "personal_photo" : base64.b64encode(photo_data).decode("utf-8") if photo_data else None,
            "national_ID_photo" : base64.b64encode(national_photo_data).decode("utf-8") if national_photo_data else None,
        }
    )
    return Response(user_profile)
    
def student_view_profile(user, user_profile: dict):
    student = Student.objects.get(student=user)
    photo_data = student.personal_photo.read() if student.personal_photo else None
    user_profile.update(
        {
            "birth_date" : student.birth_date,
            "academic_year" : student.academic_year,
            "study_field" : student.study_field,
            "parent_phone_number" : student.parent_phone_number,
            "parent_name" : student.parent_name,
            "points" : student.points,
            "balance" : student.balance,
            "verified" : student.verified,
            "personal_photo" : base64.b64encode(photo_data).decode("utf-8") if photo_data else None 
        }
    )
    return Response(user_profile)

def assistant_view_profile(user, user_profile: dict):
    assistant = Assistant.objects.get(assistant=user)
    personal_photo_data = assistant.personal_photo.read() if assistant.personal_photo else None
    national_photo_data = assistant.national_ID_photo.read() if assistant.national_ID_photo else None
    user_profile.update(
        {
            "birth_date" : assistant.birth_date,
            "personal_photo" : base64.b64encode(personal_photo_data).decode("utf-8") if personal_photo_data else None,
            "national_ID_photo" : base64.b64encode(national_photo_data).decode("utf-8") if national_photo_data else None
        }
    )
    return Response(user_profile)

#############
# Home page #
#############

@login_required
@api_view(['GET'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def home(request):
    return Response("Home Page")