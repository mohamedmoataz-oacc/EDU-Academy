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

#######################
# CSRF token endpoint #
#######################

@ensure_csrf_cookie
@api_view(['GET'])
def get_csrf_token(request):
    return Response()

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
            birth_date = data['birth_date'],
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
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if profile_is_completed(user): return redirect("api:home")
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
    
    if request.method == 'GET':
        return Response({"user_role": request.user.user_role.role})
    elif request.method == 'POST':
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

    view_self = request.user == user
    profile = {
        "view_self": view_self, # indicates whether the user searches for himself or another
        "username" : username,
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "governorate" : user.governorate,
        "email" : user.email if view_self else None,
        "date_joined" : user.date_joined,
        "gender" : user.gender,
        "phone_number" : user.phone_number if view_self else None,
        "birth_date" : user.birth_date,
        "user_role" : user.user_role.role,
    }
    return roles_to_actions[user.user_role.role]["viewing"](user, profile, view_self)


#############
# Home page #
#############

@login_required
@api_view(['GET'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def home(request):
    user = request.user
    return roles_to_actions[user.user_role.role]["home"](user)

#################
# Create course #
#################

# REMEMBER TO REMOVE PARTIAL

@login_required
@api_view(['GET', 'POST'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def create_course(request):
    if not is_accepted_teacher(request.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        required_data = {
            "required_data": [
                'subject', 'course_name', 'description','lecture_price',
                'package_size','thumbnail'
            ],
        }
        return Response(required_data)
    elif request.method == 'POST':
        serializer = CourseCreationSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        Course.objects.create(
            teacher = Teacher.objects.get(teacher=request.user),
            subject = Subject.objects.get(pk=data['subject']),
            course_name = data['course_name'],
            description = data['description'],
            lecture_price = data['lecture_price'],
            package_size = data['package_size'],
            # thumbnail = data['thumbnail']
        )
        return redirect("api:home")

################
# View Course #
###############

@api_view(['GET'])
def view_course(request, course_id:int):
    user = request.user
    return roles_to_actions[user.user_role.role]["view_course"](user, course_id)

##################
# Create lecture #
#################

@login_required
@api_view(['GET', 'POST'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def create_lecture(request, course_id:int = None):
    if not is_accepted_teacher(request.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if not len(Course.objects.filter(teacher=request.user, pk=course_id)) == 1:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        serializer = LectureCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        Lecture.objects.create(
            Lecture_title = data['Lecture_title'],
            video = data['video'],
        )    
        return redirect("api:view_lecture")

##############
# My courses #
##############

@login_required
@api_view(['GET'])
@user_passes_test(profile_is_completed, login_url="/api/complete_profile/")
def my_courses(request):
    user = request.user
    return Response(roles_to_actions[user.user_role.role]["my_courses"](user))


###############
# Get courses #
###############

@api_view(['GET'])
def get_courses(request, fields:str = "", subset=None):
    if not subset: return redirect("api:get_portion_courses", subset=1)
    fields_to_filters = {
        "subject": "subject__subject_name",
        "teacher": "teacher__teacher__username",
        "completed": "completed",
    }
    fields = fields.split("&")
    filters = dict()
    for i in fields:
        i = i.split("=")
        if len(i) != 2 or i[0] not in fields_to_filters: continue
        filters[fields_to_filters[i[0]]] = i[1]
    
    all_courses = Course.objects.all()
    all_courses = all_courses.filter(**filters)[20*(subset-1):20*subset]
    
    filtered_courses = [
        {
            "id": course.id,
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            # "thumbnail": course.thumbnail,
            "subject": course.subject.subject_name,
        } for course in all_courses
    ]
    return Response(filtered_courses)