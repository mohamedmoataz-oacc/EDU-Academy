from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from .serializers import *
from eduAcademy.views_checks import *

###########
# Sign up #
###########

@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return Response({"detail": "You are already logged in"}, status=status.HTTP_403_FORBIDDEN)
    
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
            birth_date = data['birth_date'],
            user_role=UsersRole.objects.get(pk=data['user_role']),
        )
        return Response({"detail": "Signup successful"})
        
##################
# Login & Logout #
##################


@ensure_csrf_cookie
@api_view(['GET', 'POST'])
def login_user(request):
    if request.user.is_authenticated:
        return Response({"detail": "You are already logged in"}, status=status.HTTP_403_FORBIDDEN)
    
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
                return Response({
                        "detail":"User logged in successfully",
                        "user_role": user.user_role.role
                    }
                )
            else:
                return Response({
                        "detail":"User logged in successfully and profile is incompleted",
                        "redirect_to": "/CompleteProfile",
                        "user_role": user.user_role.role
                    }
                )
        else:
            return Response({"detail": "The username or password is incorrect."}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        return Response()

@api_view(['GET', 'POST'])
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response({"detail": "User logged out successfully."})
    return Response({"detail": "Logging out must be done via a POST request."})

############
# Facebook #
############

# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter


##########
# Google #
##########

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter