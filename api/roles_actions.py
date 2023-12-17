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


# REMEMBER TO REMOVE PARTIAL

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
        serializer = TeacherProfileSerializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
        
        Teacher.objects.create(
            teacher = request.user,
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
        
        Student.objects.create(
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
        
        Assistant.objects.create(
            assistant=request.user,
            birth_date = data['birth_date'],
            # personal_photo = data['personal_photo'],
            # national_ID_photo = data['national_ID_photo'],
        ).save()
        return redirect("api:view_profile", username=request.user.username)


###################
# Profile viewing #
###################

def teacher_view_profile(user, user_profile: dict):
    teacher = Teacher.objects.get(teacher=user)
    user_profile.update(
        {
            "balance" : teacher.balance,
            "accepted" : teacher.accepted,
            "personal_photo" : teacher.personal_photo,
            "national_ID_photo" : teacher.national_ID_photo,
        }
    )
    return Response(user_profile)
    
def student_view_profile(user, user_profile: dict):
    student = Student.objects.get(student=user)
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
            "personal_photo" : student.personal_photo
        }
    )
    return Response(user_profile)

def assistant_view_profile(user, user_profile: dict):
    assistant = Assistant.objects.get(assistant=user)
    user_profile.update(
        {
            "birth_date" : assistant.birth_date,
            "personal_photo" : assistant.personal_photo,
            "national_ID_photo" : assistant.national_ID_photo,
        }
    )
    return Response(user_profile)


########
# Home #
########

def teacher_home(user):
    return Response("Home Page")

def student_home(user):
    enrolled_courses = student_my_courses(user)
    student = Student.objects.get(student=user)
    courses = Course.objects.all().difference(student.course_set.all())[:20]

    not_enrolled_courses = [
        {
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            # "thumbnail": course.thumbnail,
            "subject": course.subject.subject_name,
        } for course in courses
    ]

    output = {
        "enrolled_courses": enrolled_courses,
        "not_enrolled_courses": not_enrolled_courses,
    }

    return Response(output)

def assistant_home(user):
    return Response("Home Page")


##############
# My courses #
##############

def teacher_my_courses(user):
    teacher = Teacher.objects.get(teacher=user)
    courses = teacher.course_set.all()
    output = [
        {
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "creation_date": course.creation_date.date(),
            # "thumbnail": course.thumbnail,
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    return output

def student_my_courses(user):
    student = Student.objects.get(student=user)
    courses = student.course_set.all()
    output = [
        {
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "enrolled_date": Enrollment.objects.get(course=course, student=student).start_date.date(),
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            # "thumbnail": course.thumbnail,
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    return output

def assistant_my_courses(user):
    assistant = Assistant.objects.get(assistant=user)
    courses = assistant.course_set.all()
    output = [
        {
            "name": course.course_name,
            "description": course.description,
            "is_completed": course.completed,
            "assisting_date": Assisting.objects.get(course=course, assistant=assistant).start_date.date(),
            "teacher": User.objects.get(pk=course.teacher.pk).first_name + " " +
                       User.objects.get(pk=course.teacher.pk).last_name,
            # "thumbnail": course.thumbnail,
            "subject": course.subject.subject_name,
        } for course in courses
    ]
    return output

####################
# Roles -> actions #
####################

roles_to_actions = {
    "Teacher": {
        "completion": teacher_complete_profile,
        "viewing": teacher_view_profile,
        "home": teacher_home,
        "my_courses": teacher_my_courses,
    },
    "Student": {
        "completion": student_complete_profile,
        "viewing": student_view_profile,
        "home": student_home,
        "my_courses": student_my_courses,
    },
    "Assistant": {
        "completion": assistant_complete_profile,
        "viewing": assistant_view_profile,
        "home": assistant_home,
        "my_courses": assistant_my_courses,
    },
}