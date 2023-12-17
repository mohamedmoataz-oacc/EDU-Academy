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
from .roles_actions import *
from .views_checks import *
from .serializers import *

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
    return roles_to_actions[request.user.user_role.role]["completion"](request)


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
    return roles_to_actions[user.user_role.role]["viewing"](user, profile)


#############
# Home page #
#############

@login_required
@api_view(['GET'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def home(request):
    user = request.user
    return roles_to_actions[user.user_role.role]["home"](user)

########
# course operations #
########

@login_required
@api_view(['GET', 'POST'])
@user_passes_test(is_teacher, login_url="/api/complete_profile/")
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def create_course(request):
    if request.method == 'GET':
        required_data = {
            "required_data": [
                'subject', 'course_name', 'description','lecture_price',
                'package_size','thumbnail'
            ],
        }
        return Response(required_data)
    elif request.method == 'POST':
        serializer = CourseCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        Course.objects.create(
            teacher=request.user,
            subject = data['subject'],
            course_name = data['course_name'],
            description = data['description'],
            lecture_price = data['lecture_price'],
            package_size = data['package_size'],
            thumbnail = data['thumbnail']
        )
        return redirect("api:home")