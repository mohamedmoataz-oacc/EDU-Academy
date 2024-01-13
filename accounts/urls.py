from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordResetView, PasswordChangeView
from django.urls import path
from .views import SignUpView, profile_completed


urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("profile-completed/", profile_completed, name="profile_completed"),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name="account_confirm_email"),
    path('account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path("register/", SignUpView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    path("request-password-reset/", PasswordResetView.as_view(), name="request_password_reset"),
    path("change-password/", PasswordChangeView.as_view(), name="change_password"),
]