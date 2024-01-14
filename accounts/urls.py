from django.urls import path
from .views import SignUpView, EmailVerificationView, profile_completed

from dj_rest_auth.views import (
    LoginView, LogoutView, UserDetailsView, PasswordResetView, PasswordResetConfirmView,
)


urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("profile-completed/", profile_completed, name="profile_completed"),
    path('account-confirm-email/<str:key>/', EmailVerificationView.as_view(), name="account_confirm_email"),
    path('account-confirm-email/', EmailVerificationView.as_view(), name='account_email_verification_sent'),
    path("register/", SignUpView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),

    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]