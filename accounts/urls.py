from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordResetView, PasswordChangeView
from django.urls import path


urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("request_password_reset/", PasswordResetView.as_view(), name="request_password_reset"),
    path("change_password/", PasswordChangeView.as_view(), name="change_password"),
    path("verify_email/", VerifyEmailView.as_view(), name="verify_email"),
]