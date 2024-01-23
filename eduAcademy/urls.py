"""
URL configuration for eduAcademy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/profile/', include('profiles.urls')),
    path('api/credits/', include('payment_credits.urls')),

    path('', views.index, name='index'),
    path('accounts/login', views.index, name='frontend_login'),
    path('profile/complete-profile', views.index, name='frontend_complete_profile'),
    path('profile', views.index, name='frontend_profile'),
    path('home', views.index, name='frontend_home'),
    path('courses/create-course', views.index, name='frontend_create_course'),
    path('accounts/password-reset-confirm', views.index, name='frontend_password_reset_confirm'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
