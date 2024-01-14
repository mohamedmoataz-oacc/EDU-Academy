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

    path('', views.index, name='index1'),
    path('Login', views.index, name='index2'),
    path('CompleteProfile', views.index, name='index3'),
    path('Profile', views.index, name='index4'),
    path('Home', views.index, name='index5'),
    path('Createcourse', views.index, name='index6'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
