from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
# return bad_request(request, "Either the username or email address is already associated with an account.")
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
from .views_checks import *
from .serializers import *

import base64
# What views do we want to create

# First, authentication & authorization:
# 1. Signup
# 2. Login
# 3. Profile viewing & profile completion

# Then we will need to track the user's session to be able to authorize him

# Other functionalities:
# 1. See all courses and be able to filter by subject and grade
# 2. See all teachers and be able to filter by subject and grade
# 3. Get the student's points

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("api:complete_profile"))
    
    if request.method == 'GET':
        return Response()
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
            user_role=UsersRole.objects.get(pk=data['user_role'])
        )
        return HttpResponseRedirect(reverse("api:login"))
        
@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("api:complete_profile"))
    
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
                return HttpResponseRedirect(reverse("api:home"))
            else: return HttpResponseRedirect(reverse("api:complete_profile"))
        else:
            return Response(data="The username or password is incorrect.", status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        return Response()
    
@login_required
@api_view()
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("api:login"))

@login_required
@api_view()
def complete_profile(request):
    if profile_is_completed(request.user):
        return HttpResponseRedirect(reverse("api:home"))
    
    roles_to_profiles = {
        "Teacher": teacher_complete_profile,
        "Student": student_complete_profile,
        "Assistant": assistant_complete_profile
    }

    return roles_to_profiles[request.user.user_role.role](request)


def teacher_complete_profile(request): ...

def student_complete_profile(request): ...

def assistant_complete_profile(request): ...

@login_required
@api_view()
@user_passes_test(profile_is_completed, login_url=reverse("api:complete_profile"))
def view_profile(request, name):

    user = get_object_or_404(User, username=name)
    
    roles_to_profiles = {
        "Teacher": teacher_complete_profile,
        "Student": student_complete_profile,
        "Assistant": assistant_complete_profile
    }
    profile = {
        "view_self": request.user == user, # indicates whether the user searches for himself or another
        "username" : name,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "governorate" : user.governorate,
        "email" : user.email,
        "date_joined" : user.date_joined,
        "gender" : user.gender,
        "phone_number" : user.phone_number,
        "user_role" : user.user_role.role
    }
    return roles_to_profiles[user.user_role.role](request, user, profile)

def teacher_view_profile(request, user, user_profile: dict):
    teacher = Teacher.objects.get(teacher=user)
    photo_data = teacher.personal_photo.read() if teacher.personal_photo else None
    user_profile.update(
        {
            "balance" : teacher.balance,
            "accepted" : teacher.accepted,
            "personal_photo" : base64.b64encode(photo_data).decode("utf-8") if photo_data else None
        }
    )
    return Response(user_profile)
    

def student_view_profile(request, user, user_profile: dict):
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


def assistant_view_profile(request, user, user_profile: dict):
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

@login_required
@api_view()
@user_passes_test(profile_is_completed, login_url=reverse("api:complete_profile"))
def home(request): ...