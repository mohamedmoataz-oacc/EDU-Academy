from django.urls import path
from .views import *

app_name = "profiles"
urlpatterns = [
    path('', view_profile, name='view_my_profile'),
    path('<str:username>/', view_profile, name='view_profile'),
    path('complete_profile/', complete_profile, name='complete_profile'),
    path('search_teacher/<str:name>', search_teacher, name='search_teacher'),
]