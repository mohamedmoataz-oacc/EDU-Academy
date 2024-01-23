from django.shortcuts import redirect
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, SocialLoginView
from dj_rest_auth.views import PasswordResetConfirmView

import eduAcademy.settings as app_settings
from .serializers import *
from eduAcademy.views_checks import *
from .adapters.oauthadapters import CustomGoogleOAuth2Adapter, CustomFacebookOAuth2Adapter

class SignUpView(RegisterView):
    serializer_class = SignupSerializer

class EmailVerificationView(VerifyEmailView):
    def get(self, request, **kwargs):
        if app_settings.ACCOUNT_CONFIRM_EMAIL_ON_GET:
            request.method = 'POST'
            request.data.update(kwargs)
            self.post(request, **kwargs)
        return redirect('index')

class RedirectPasswordResetConfirmView(PasswordResetConfirmView):
    def get(self, request, uidb64, token):
        url = f"{reverse('frontend_password_reset_confirm')}?token={token}&uidb64={uidb64}"
        return redirect(url)


@api_view(['GET'])
def profile_completed(request):
    if not request.user.is_authenticated:
        return Response({"detail": "User is not authenticated"}, status=status.HTTP_403_FORBIDDEN)
    
    user = request.user
    return Response({
            "detail":f"{bool(profile_is_completed(user))}",
            "user_role": user.user_role.role,
        }
    )

############
# Facebook #
############

class FacebookLogin(SocialLoginView):
    adapter_class = CustomFacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = app_settings.SITE_URL + "/api/accounts/facebook/"


##########
# Google #
##########

class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = app_settings.SITE_URL + "/api/accounts/google/"
    client_class = OAuth2Client