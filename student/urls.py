"""
URL configuration for student project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from userapp import views as user_views
from adminapp import views as admin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_views.index,name="index"),
    path('about',user_views.about,name="about"),
    path('contact',user_views.contact,name="contact"),
    path('services',user_views.services,name="services"),
    path('admin-login',user_views.admin_login,name="admin_login"),
    path('user-dashboard',user_views.user_dashboard,name="user_dashboard"),
    path('register',user_views.UserRegister, name ='register'),
    path('login',user_views.UserLogin, name ='login'),
    path('user-profile',user_views.user_profile,name="user_profile"),
    path('student',user_views.student,name="student"),



    path('admin-dashboard',admin_views.index,name="admin_dashboard"),
    path('upload-dataset',admin_views.upload_dataset,name="upload_dataset"),
    path('view-dataset/',admin_views.view_dataset,name="view_dataset"),
    path('attacks-analysis',admin_views.attacks_analysis,name="attacks_analysis"),
    path('Logistic-Regression',admin_views.alg4,name="alg4"),
    path('logout',user_views.user_logout,name="log_out"),



]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
