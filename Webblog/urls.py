"""Webblog URL Configuration

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
from django.urls import path, re_path, include

import blog
from blog.views import write_blog_entry, read_blog_entry, read, GrantBlogView, CompileBlogEntry, TestView, index, \
    indexview, Profile
from userinfo.views import RegisterView, LoginView, UserInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("write_blog_entry/", write_blog_entry),
    path("read_blog_entry/", read_blog_entry),
    path("read_blog/", read)
]

urlpatterns += [
    path("", indexview),
    path("index/<int:page>/", index),
    path("login/", LoginView.as_view()),
    path("register/", RegisterView.as_view()),
    path("user_info/", UserInfoView.as_view()),
    path("grant_blog/", GrantBlogView.as_view() ),
    path("compile_blog/", CompileBlogEntry.as_view()),
    path("profile/", Profile),
    re_path(r'^test/(?P<username>\w+)/$', TestView.as_view()),
    re_path(r"(?P<username>\w+)/", include("blog.urls"))

]