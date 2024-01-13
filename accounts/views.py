from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from dj_rest_auth.registration.views import RegisterView

from .serializers import *
from eduAcademy.views_checks import *

###########
# Sign up #
###########

class SignUpView(RegisterView):
    serializer_class = SignupSerializer


@ensure_csrf_cookie
@api_view(['GET'])
def profile_completed(request):
    if not request.user.is_authenticated:
        return Response({"detail": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    return Response({
            "detail":f"{bool(profile_is_completed(user))}",
            "user_role": user.user_role.role
        }
    )

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