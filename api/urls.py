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
    path('get_courses/<int:subset>/<str:fields>/', get_courses, name='get_filtered_courses'),
    path('get_courses/<int:subset>/', get_courses, name='get_portion_courses'),
    path('get_courses/', get_courses, name='get_all_courses'),
    path('course/<int:course_id>/', view_course, name='view_course'),
    path('course/<int:course_id>/create_lecture/', create_lecture, name='create_lecture'),
    path('course/<int:course_id>/<str:lecture_title>/', view_lecture, name='view_lecture'),
]