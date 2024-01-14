from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import redirect

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView

import eduAcademy.settings as app_settings
from .serializers import *
from eduAcademy.views_checks import *

class SignUpView(RegisterView):
    serializer_class = SignupSerializer

class EmailVerificationView(VerifyEmailView):
    def get(self, request, **kwargs):
        if app_settings.ACCOUNT_CONFIRM_EMAIL_ON_GET:
            request.method = 'POST'
            request.data.update(kwargs)
            self.post(request, **kwargs)
        return redirect('index1')

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