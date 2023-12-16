"""
Contains functions for the actions that are different between user roles.
"""

from django.shortcuts import redirect
from rest_framework.response import Response
from .serializers import *
import base64

# Note that `request.FILES` will only contain data if the request method was POST,
# at least one file field was actually posted,
# and the <form> that posted the request has the attribute enctype="multipart/form-data".
# Otherwise, `request.FILES` will be empty.


######################
# Profile completion #
######################

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

########
# Home #
########
def teacher_home(user):
    return Response("Home Page")

def student_home(user):
    return Response("Home Page")

def assistant_home(user):
    return Response("Home Page")


####################
# Roles -> actions #
####################

roles_to_actions = {
    "Teacher": {
        "completion": teacher_complete_profile,
        "viewing": teacher_view_profile,
        "home": teacher_home,
    },
    "Student": {
        "completion": student_complete_profile,
        "viewing": student_view_profile,
        "home": student_home,
    },
    "Assistant": {
        "completion": assistant_complete_profile,
        "viewing": assistant_view_profile,
        "home": assistant_home,
    },
}