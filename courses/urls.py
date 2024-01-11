from django.urls import path
from .views import *

app_name = "courses"
urlpatterns = [
    path('create_course/', create_course, name='create_course'),
    path('my_courses/', my_courses, name='my_courses'),
    path('get_courses/<int:subset>/', get_courses, name='get_portion_courses'),
    path('get_courses/', get_courses, name='get_all_courses'),
    path('get_subjects/', get_subjects, name='get_subjects'),
    path('<int:course_id>/', view_course, name='view_course'),
    path('<int:course_id>/create_lecture/', create_lecture, name='create_lecture'),
    path('<int:course_id>/<str:lecture_slug>/', view_lecture, name='view_lecture'),
    path('search_course/<str:name>', search_course, name='search_course'),
]