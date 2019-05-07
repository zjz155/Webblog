from django.urls import path, re_path

import blog
from blog.views import TestView, read_blog_entry, DetialEntryView, ListEntryView
from userinfo.views import RegisterView, LoginView, UserInfoView

urlpatterns = [

]

urlpatterns += [
    re_path(r"article/$", ListEntryView.as_view()),
    re_path(r"article/details/(?P<article_id>\d+)/$", DetialEntryView.as_view()),
    re_path(r"article/details/(?P<article_id>\d+)/data/$", read_blog_entry),

]