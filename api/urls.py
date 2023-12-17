from django.urls import path
from .views import *

app_name = "api"
urlpatterns = [
    path('csrf/', get_csrf_token, name='csrf'),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('complete_profile/', complete_profile, name='complete_profile'),
    path('home/', home, name='home'),
    path('view_profile/', view_profile, name='view_my_profile'),
    path('view_profile/<str:username>/', view_profile, name='view_profile'),
    path('create_course/', create_course, name='create_course'),
    path('my_courses/', my_courses, name='my_courses'),
]