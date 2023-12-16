from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.request import HttpRequest

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import *

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

roles_to_models = {"Teacher": Teacher, "Student": Student, "Assistant": Assistant}

@ensure_csrf_cookie
def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("home")
    
    if request.method == 'GET':
        return HttpResponse()
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
            return HttpResponse("Sign up has been successful.")
        except IntegrityError:
            return HttpResponseBadRequest("Either the username or email address is already associated with an account.")

@ensure_csrf_cookie
# @api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("home")
    
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if len(roles_to_models.get(user.user_role.role).objects.get(pk=user.pk)) == 0:
                return HttpResponseRedirect("complete_profile")
            else: return HttpResponseRedirect("home")
        else:
            return Http404("The email or password is incorrect.")
    elif request.method == 'GET':
        return HttpResponse()
    
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("login")

@login_required
def complete_profile(request): ...

@ensure_csrf_cookie
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