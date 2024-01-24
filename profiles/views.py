from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .roles_actions import roles_to_actions
from eduAcademy.views_checks import *
from accounts.models import User
from .serializers import *


def authenticate_user(user):
    if not user.is_authenticated:
        return Response(
            {
                "detail":"User should log in first to complete his profile",
                "redirect_to": reverse("frontend_login")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

######################
# Profile completion #
######################

@ensure_csrf_cookie
@api_view(['POST'])
def complete_user_role(request):
    authenticated = authenticate_user(request.user)
    if authenticated: return authenticated
    
    serializer = UserRoleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
    user = request.user
    user.user_role = UsersRole.objects.get(pk=data['user_role'])
    user.save()
    return Response({"detail": "Role completed successfully"})

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def complete_profile(request):
    authenticated = authenticate_user(request.user)
    if authenticated: return authenticated
    if request.user.user_role is None:
        return Response(
            {
                "detail":"User should have a role to complete his profile",
                "redirect_to": reverse("profiles:complete_user_role")
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    if profile_is_completed(request.user):
        return Response(
            {"detail": "The user's profile has been already completed"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        all_fields = [f.name for f in User._meta.get_fields()]
        extra = []
        for i in all_fields:
            try:
                if getattr(request.user, i) is None: extra.append(i)
            except: pass
        return Response({
            "user_role": request.user.user_role.role,
            "extra_data": extra
        })
    elif request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if serializer.data.get('governorate') and request.user.governorate is None:
                request.user.governorate = serializer.data.get('governorate')
            if serializer.data.get('phone_number') and request.user.phone_number is None:
                request.user.phone_number = serializer.data.get('phone_number')
        request.user.save()
        return roles_to_actions[request.user.user_role.role]["completion"](request)


###################
# Profile viewing #
###################

@api_view(['GET'])
def view_profile(request, username=None):
    authenticated = authenticate_user(request.user)
    if authenticated: return authenticated
    if not profile_is_completed(request.user):
        role = request.user.user_role
        return Response({
                "detail":"User should complete his account to view profiles",
                "redirect_to": reverse("profiles:complete_profile") if role else reverse("profiles:complete_user_role"),
                "user_role": role.role if role else None,
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    username = request.GET.get("username") or request.user.username
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

###################
# Teachers search #
###################

@api_view(['GET'])
def search_teacher(request, name):
    teachers_matched = Teacher.objects.filter(teacher__full_name__icontains=name)
    teachers = [
        {
            "personal_photo" : str(teacher.personal_photo),
            "name": teacher.full_name,
            "subjects": [i.subject_name for i in teacher.subject_set.all()],
        } for teacher in teachers_matched
    ]
    return Response(teachers)