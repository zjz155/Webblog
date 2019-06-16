from django.urls import path, re_path

from blog.views import DetialEntryView, ReadBlogEntry, IndexView
from userinfo.views import ContactView

urlpatterns = [

]

urlpatterns += [
    re_path(r"article/(?P<data>\w+)/$", IndexView.as_view(), name="entry-list"),
    #
    re_path(r"article/details/(?P<article_id>\d+)/$", DetialEntryView.as_view(), name="post-detail"),
    re_path(r"article/details/(?P<article_id>\d+)/data/$", ReadBlogEntry.as_view()),
    # 关注
    re_path(r"contact/(?P<action>\w+)/(?P<be_followed>\w+(-*)\w+)/$", ContactView.as_view()),


]