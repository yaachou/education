"""education_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from parents import views

app_name = 'parents'

urlpatterns = [
    path('index.html/', views.index),
    
    path('register.html/', views.register, name='register'),
    path('register.html/register_check/', views.register_check, name='register_check'),
    path('register_parent.html/', views.register_parent),
    path('register_teacher.html/', views.register_teacher),
    path('register_agency.html/', views.register_agency),
    path('registering/', views.get_regi_info, name='get_regi_info'),

    path('login.html/', views.login, name='login'),
    path('login.html/login_check/', views.login_check, name='login_check'),
    
    path('display_info/', views.display_info, name='display_info'),
    path('alter_info/', views.alter_info, name='alter_info'),
    
    path('seek_lessons/', views.seek_lessons, name='seek_lessons'),
    path('display_lessons/', views.display_lessons, name='display_lessons'),
    
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('get_cart/', views.get_cart, name='get_cart'),

    path('pay/', views.pay, name='pay'),
    
    path('logout/', views.logout, name='logout'),
]
