from django.urls import path
from .views import *

app_name = "api"
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('complete_profile/', complete_profile, name='complete_profile'),
    path('home/', home, name='home'),
]