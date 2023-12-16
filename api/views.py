from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import bad_request
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *
from .views_checks import *
from .serializers import LoginSerializer

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
        return HttpResponseRedirect("home/")
    
    if request.method == 'GET':
        return Response()
    elif request.method == 'POST':
        try:
            User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                governorate=request.POST['governorate'],
                phone_number=request.POST['phone_number'],
                gender=request.POST['gender']
            )
            return HttpResponseRedirect(reverse("api:login"))
        except IntegrityError:
            return bad_request(request, "Either the username or email address is already associated with an account.")

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("api:home"))
    
    if request.method == 'POST':
        print("This is a post")
        serializer = LoginSerializer(data=request.data)
        # if serializer.is_valid(raise_exception=True):
        #     d = serializer.data()
        data = serializer.initial_data
        username = data["username"]
        password = data["password"]
        print("Found 1")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("Found 2")
            login(request, user)

            if profile_is_completed(user):
                return HttpResponseRedirect(reverse("api:home"))
            else: return HttpResponseRedirect(reverse("api:complete_user_profile", args=(user.user_role.role,)))
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
def view_profile(request): ...
@login_required
def home(request): ...