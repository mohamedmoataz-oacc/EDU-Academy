from django.urls import path
from .views import (
    SignUpView, EmailVerificationView, RedirectPasswordResetConfirmView, profile_completed,
    GoogleLogin, FacebookLogin,
)
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path("profile-completed/", profile_completed, name="profile_completed"),
    path('account-confirm-email/<str:key>/', EmailVerificationView.as_view(), name="account_confirm_email"),
    path('account-confirm-email/', EmailVerificationView.as_view(), name='account_email_verification_sent'),
    path("register/", SignUpView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path('password-reset/', PasswordResetView.as_view(), name="account_reset_password"),
    path('password-reset-confirm/<uidb64>/<token>/', RedirectPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm_frontend'),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("facebook/", FacebookLogin.as_view(), name="facebook_login"),
]