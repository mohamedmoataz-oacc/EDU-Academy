"""
Contains functions for the actions that are different between user roles.
"""

from django.urls import reverse
from rest_framework.response import Response
from .serializers import *
from eduAcademy.views_checks import *
from .models import *


######################
# Profile completion #
######################

def teacher_complete_profile(request):
    data = {**request.data, **request.FILES}
    data = {i:j[0] if isinstance(j, list) else j for i, j in data.items()}

    serializer = TeacherProfileSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    teacher = Teacher.objects.create(
        teacher = request.user,
        personal_photo = data['personal_photo'],
        national_ID_photo = data['national_ID_photo'],
    )
    TeachRequest.objects.create(teacher=teacher)
    return Response({
            "detail":"Teacher completed profile successfully",
            "user_role":request.user.user_role.role,
            "username":request.user.username,
            "redirect_to": reverse("frontend_profile")
        }
    )

def student_complete_profile(request):
    data = {**request.data, **request.FILES}
    data = {i:j[0] if isinstance(j, list) else j for i, j in data.items()}

    serializer = StudentProfileSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    
    Student.objects.create(
        student=request.user,
        academic_year = data['academic_year'],
        study_field = data.get('study_field'),
        parent_name = data['parent_name'],
        parent_phone_number = data['parent_phone_number'],
        personal_photo = data.get('personal_photo'),
    )
    return Response({
            "detail":"Student completed profile successfully",
            "user_role":request.user.user_role.role,
            "username":request.user.username,
            "redirect_to": reverse("frontend_profile")
        }
    )

def assistant_complete_profile(request):
    data = {**request.data, **request.FILES}
    data = {i:j[0] if isinstance(j, list) else j for i, j in data.items()}

    serializer = AssistantProfileSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    
    Assistant.objects.create(
        assistant=request.user,
        personal_photo = data['personal_photo'],
        national_ID_photo = data['national_ID_photo'],
    )

    return Response({
            "detail":"Assistant completed profile successfully",
            "user_role":request.user.user_role.role,
            "username":request.user.username,
            "redirect_to": reverse("frontend_profile")
        }
    )


###################
# Profile viewing #
###################

def teacher_view_profile(user, user_profile: dict, view_self):
    teacher = Teacher.objects.get(teacher=user)
    user_profile.update(
        {
            "balance" : teacher.balance if view_self else None,
            "accepted" : teacher.accepted,
            "personal_photo" : f"media/{teacher.personal_photo}",
            "national_ID_photo" : f"media/{teacher.national_ID_photo}" if view_self else None,
        }
    )
    return Response(user_profile)
    
def student_view_profile(user, user_profile: dict, view_self):
    student = Student.objects.get(student=user)
    badges_list = student.badge_set.all()
    user_profile.update(
        {
            "academic_year" : student.academic_year,
            "study_field" : student.study_field,
            "parent_phone_number" : student.parent_phone_number,
            "parent_name" : student.parent_name,
            "points" : student.points if view_self else None,
            "balance" : student.balance if view_self else None,
            "personal_photo" : f"media/{student.personal_photo}" if student.personal_photo else None,
            "badges" : [badge.badge_name for badge in badges_list]
        }
    )
    return Response(user_profile)

def assistant_view_profile(user, user_profile: dict, view_self):
    assistant = Assistant.objects.get(assistant=user)
    user_profile.update(
        {
            "personal_photo" : f"media/{assistant.personal_photo}",
            "national_ID_photo" : f"media/{assistant.national_ID_photo}" if view_self else None,
        }
    )
    return Response(user_profile)


####################
# Roles -> actions #
####################

roles_to_actions = {
    "Teacher": {
        "completion": teacher_complete_profile,
        "viewing": teacher_view_profile,
    },
    "Student": {
        "completion": student_complete_profile,
        "viewing": student_view_profile,
    },
    "Assistant": {
        "completion": assistant_complete_profile,
        "viewing": assistant_view_profile,
    },
}