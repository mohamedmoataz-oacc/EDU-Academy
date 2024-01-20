from django.urls import path
from .views import *

app_name = "profiles"
urlpatterns = [
    path('', view_profile, name='view_my_profile'),
    path('complete-user-role/', complete_user_role, name='complete_user_role'),
    path('complete-profile/', complete_profile, name='complete_profile'),
    path('search-teacher/<str:name>', search_teacher, name='search_teacher'),
]