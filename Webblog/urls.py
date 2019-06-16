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
from django.views.generic import RedirectView

import blog
from blog.views import GrantBlogView, CompileBlogEntry, TestView, IndexView, CommentView, ReplyView
from userinfo.views import RegisterView, LoginView, IsVailTokenView, UserInfoView

urlpatterns = [
    path('admin/', admin.site.urls),

]

urlpatterns += [

    path("", RedirectView.as_view(url="/blog/jz_zhou/article/list")),
    # re_path(r"blog/(?P<username>\w+(-*)\w+)/(?P<data>\w+)/$", IndexView.as_view(), name="entry-list"),
    re_path(r"blog/(?P<username>\w+(-*)\w+)/", include("blog.urls")),
    # path("index/<int:page>/", index),
    path("login/", LoginView.as_view()),
    path("is_login/", IsVailTokenView.as_view()),
    path("register/", RegisterView.as_view()),
    path("grant_blog/", GrantBlogView.as_view()),

    re_path(r'^test/(?P<username>\w+)/$', TestView.as_view()),

    re_path(r"(?P<username>\w+(_*)\w+)/comment/(?P<article_id>\w+)/$", CommentView.as_view()),
    re_path(r"comment/list/(?P<article_id>\w+)/(?P<page>\w+)/$", CommentView.as_view()),
    re_path(r"reply_list/(?P<comment_id>\w+)/(?P<page>\w+)/$", ReplyView.as_view()),
    re_path(r"reply/(?P<username>\w+(-*)\w+)/reply/(?P<comment_id>\w+)/$", ReplyView.as_view()),

    re_path("compile_blog/(?P<username>\w+(-*)\w+)/$", CompileBlogEntry.as_view()),
    re_path("userinfo/(?P<username>\w+(-*)\w+)/$", UserInfoView.as_view()),


]