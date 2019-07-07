"""EducationOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include
from django.conf.urls import url
from agency.views import *
app_name = 'agency'
urlpatterns = [
    path('agency_index/',AgencyIndex.as_view() ,name='agency_index'),  #import agency url
    path('teacher_index/',TeacherIndex.as_view() ,name='teacher_index'),  #import agency url
    path('register_teacher/',TeacherRegister.as_view(),name='register_teacher'),
    path('register_agency/',AgencyRegister.as_view(),name='register_agency'),
    path('notice_list/',DisplayNotice.as_view(),name='notice_list'),  
    path('notice_add/',AddNotice.as_view(),name='notice_add'),   
    path('apply_list/',ApplyList.as_view(),name='apply_list'),
    path('lesson_list/',LessonList.as_view(),name='lesson_list'),
    path('lesson_add/',AddLesson.as_view(),name='lesson_add'),
    path('lesson_delete/',lesson_delete,name='lesson_delete'), 
    path('lesson_edit/<int:pk>/',lesson_detail,name='lesson_edit'),
    path('lesson_detail/<int:pk>/',lesson_detail,name='lesson_detail'),
    path('notice_delete/',notice_delete,name='notice_delete'), 
    path('price_edit/<int:pk>',change_price,name='price_edit'), 
]
