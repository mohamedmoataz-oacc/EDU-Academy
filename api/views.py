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
        return HttpResponseRedirect(reverse("api:home"))
    
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
        return HttpResponseRedirect(reverse("api:home"))
    
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
@api_view(['GET', 'POST'])
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("api:login"))

@login_required
@api_view(['GET', 'POST'])
def complete_profile(request):
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
def view_profile(request, name):
    if request.method == 'POST':
        return HttpResponseBadRequest("only GET requests")
    
    user = get_object_or_404(User, username=name)
    profile = {
                "username" : name,
                "first_name" : user.first_name,
                "last_name" : user.last_name,
                "governorate" : user.governorate,
                "email" : user.email,
                "date_joined" : user.date_joined,
                "gender" : user.gender,
                "phone_number" : user.phone_number,
                "user_role" : user.user_role
            }
    return JsonResponse(profile)

@login_required
def home(request): ...