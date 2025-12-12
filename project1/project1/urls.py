"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from basic.views import login,  signUp, sample, sampleInfo, dynamicResponse , health , addStudent , job1 ,job2 ,signup,check
from basic.views import getAllusers



urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/',sample),
    path('info/',sampleInfo),
    path('dynamic/',dynamicResponse),
    path('health/',health),
    path('student/',addStudent),
    path("signup/", signup),
    path("job1/",job1),
    path("job2/", job2),
    path("signUp/",signUp),
    path("check/",check),
    path("login/",login), 
    path("users/",getAllusers),
    
]