from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse
from django.db.models import F
  
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .roles_actions import roles_to_actions, get_basic_course_info
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
        return Response(data="You are already logged in", status=status.HTTP_403_FORBIDDEN)
    
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
        return Response("Signup successful")
        
##################
# Login & Logout #
##################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return Response(data="You are already logged in", status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        username = data["username"]
        password = data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if profile_is_completed(user):
                return Response({"message":"User logged in successfully",
                                 "user_role": user.user_role.role})
            else:
                return Response({"message":"User logged in successfully and profile is incompleted",
                                 "redirect_to": "/CompleteProfile",
                                  "user_role": user.user_role.role})
        else:
            return Response(data="The username or password is incorrect.", status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        required_data = {
            "required_data": ['username', 'password'],
        }
        return Response(required_data)

@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response("User logged out successfully")

######################
# Profile completion #
######################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def complete_profile(request):
    if not request.user.is_authenticated:
        Response({"message":"User should log in first to complete his profile",
                  "redirect_to": reverse("api:login")}, status=status.HTTP_401_UNAUTHORIZED)
    if profile_is_completed(request.user):
        return Response(data="The user's profile has been already completed", status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        return Response({"user_role": request.user.user_role.role})
    elif request.method == 'POST':
        return roles_to_actions[request.user.user_role.role]["completion"](request)


###################
# Profile viewing #
###################

@api_view(['GET'])
def view_profile(request, username=None):
    if not request.user.is_authenticated:
        Response({"message":"User should log in first to view profiles",
                  "redirect_to": reverse("api:login")},
                  status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({"message":"User should complete his account view profiles",
                         "redirect_to": reverse("api:complete_profile"),
                          "user_role": request.user.user_role.role})
    if username is None:
        return Response({"redirect_to": reverse("api:view_profile", args=request.user.username)})
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

@api_view(['GET'])
def home(request):
    user = request.user
    return roles_to_actions[user.user_role.role]["home"](user)

#################
# Create course #
#################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def create_course(request):
    if not request.user.is_authenticated:
        Response({"message":" The user is not authenticated to create a course",
                  "redirect_to": reverse("api:login")},
                  status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({"message":"User should complete his profile",
                         "redirect_to": reverse("api:complete_profile"),
                           "user_role": request.user.user_role.role})
    if not is_accepted_teacher(request.user):
        return Response(data="The teacher request either is still not reviwed or was rejected", status=status.HTTP_401_UNAUTHORIZED)
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
            teacher = Teacher.objects.get(teacher=request.user),
            subject = Subject.objects.get(pk=data['subject']),
            course_name = data['course_name'],
            description = data['description'],
            lecture_price = data['lecture_price'],
            package_size = data['package_size'],
            thumbnail = data['thumbnail']
        )
        return Response("The course has been created successfully")

###############
# View Course #
###############

@api_view(['GET'])
def view_course(request, course_id:int):
    user = request.user
    if user.is_authenticated:
        return Response(roles_to_actions[user.user_role.role]["view_course"](user, course_id))
    else:
        return Response(get_basic_course_info(course_id)[0])

##################
# Create lecture #
##################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def create_lecture(request, course_id:int = None):
    if not request.user.is_authenticated:
        Response({"message":"The user is not authenticated to create a lecture",
                  "redirect_to": reverse("api:login")},
                    status=status.HTTP_401_UNAUTHORIZED)
    if not is_accepted_teacher(request.user):
        return Response(data="User should be a teacher to create a lecture",
                         status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({"message":"User should complete his profile to create a lecture",
                         "redirect_to": reverse("api:complete_profile"),
                           "user_role": request.user.user_role.role})
    course = Course.objects.filter(teacher=Teacher.objects.get(teacher=request.user), pk=course_id)
    if not course.count():
        return Response(data="Teacher is trying to create a lecture in other teacher course",
                        status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        serializer = LectureCreationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        Lecture.objects.create(
            course = course[0],
            lecture_title = data['lecture_title'],
            video = data['video'],
        )
        return Response({"message":"Lecture created successfully",
                         "redirect_to": reverse("api:view_lecture", args=(course[0].pk, data['lecture_title']))})
    elif request.method == 'GET': return Response()
    

################
# View Lecture #
################

@api_view(['GET'])
def view_lecture(request, course_id:int, lecture_title:str):
    user = request.user
    if not user.is_authenticated:
        Response({"message":"User should be logged in to view lecture",
                  "redirect_to": reverse("api:login")},
                    status=status.HTTP_401_UNAUTHORIZED)
    course = Course.objects.get(pk=course_id)
    lecture = get_object_or_404(Lecture, lecture_title=lecture_title, course=course)
    return Response(roles_to_actions[user.user_role.role]["view_lecture"](user, lecture))


####################
# Pay for lectures #
####################

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def pay_for_lecture(request, lecture_id):
    if not request.user.is_authenticated:
        return Response({"redirect_to": reverse("api:login")}, status=status.HTTP_401_UNAUTHORIZED)
    if not is_student(request.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(request.user):
        return Response({"redirect_to": reverse("api:complete_profile"), "user_role": request.user.user_role.role})
    if request.method == "GET":
        return Response()

    lecture = get_object_or_404(Lecture, pk=lecture_id)
    student = Student.objects.get(student=request.user)
    course = lecture.course
    teacher = course.teacher

    serializer = PaymentsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data

    p = Payment(
        teacher=teacher,
        lecture=lecture,
        course=course,
        student=student,
    )
    
    if data['method'] == 'balance':
        if student.balance < course.lecture_price:
            return Response(data={"detail": "Insufficient balance"}, status=status.HTTP_403_FORBIDDEN)

        p.save()
        StudentBalanceTransaction.objects.create(
            payment=p,
            student=student,
            amount=course.lecture_price,
        ).save()
        student.update(balance = F('balance') - course.lecture_price)
    elif data['method'] == 'points':
        if points_to_pounds(student.points) < course.lecture_price:
            return Response(data={"detail": "Insufficient points"}, status=status.HTTP_403_FORBIDDEN)

        p.save()
        PointsTransaction.objects.create(
            payment=p,
            student=student,
            amount=pounds_to_points(course.lecture_price),
        ).save()
        student.update(points = F('points') - pounds_to_points(course.lecture_price))
    
    if (Payment.objects.filter(student=student, course=course).count() >= 2 and
    Enrollment.objects.filter(student=student, course=course).count() == 0):
        Enrollment.objects.create(student=student, course=course)

    return Response(data={"message": "Payment successful"})


##############
# My courses #
##############

@api_view(['GET'])
def my_courses(request):
    user = request.user
    if not request.user.is_authenticated:
        Response({"message":"User should be logged in to view his courses",
                  "redirect_to": reverse("api:login")},
                    status=status.HTTP_401_UNAUTHORIZED)
    if not profile_is_completed(user):
        return Response({"message":"User should complete his profile to view his courses",
                         "redirect_to": reverse("api:complete_profile"),
                           "user_role": request.user.user_role.role})
    return Response(roles_to_actions[user.user_role.role]["my_courses"](user))


###############
# Get courses #
###############

@api_view(['GET'])
def get_courses(request, fields:str = "", subset=None):
    if not subset: return Response({"redirect_to":reverse("api:get_portion_courses", args=(1,))})
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
            "thumbnail": f"media/{course.thumbnail}",
            "subject": course.subject.subject_name,
        } for course in all_courses
    ]
    return Response(filtered_courses)