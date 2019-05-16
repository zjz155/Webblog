from django.urls import path, re_path

import blog
from blog.views import TestView, DetialEntryView, ReadBlogEntry

urlpatterns = [

]

urlpatterns += [
    re_path(r"article/details/(?P<article_id>\d+)/$", DetialEntryView.as_view(), name="post-detail"),
    re_path(r"article/details/(?P<article_id>\d+)/data/$", ReadBlogEntry.as_view()),

]