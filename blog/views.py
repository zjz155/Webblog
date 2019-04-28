from django.http import HttpResponse
from django.shortcuts import render

from blog.models import *
from common.views import check_token
from userinfo.models import UserInfo


def write_blog_entry(request, *args, **kwargs):
    if request.method == "GET":
        return render(request, "markdown.html")

    user = UserInfo.objects.filter(username="jz-zhou")
    Entry.objects.create()

    content = request.POST["content"]
    print(content)

    return HttpResponse("ok")

def read(request):
    return render(request, "read_markdown.html")

def read_blog_entry(request):
    test_entry = Test_Entry.objects.all()[0]
    content = test_entry.body_text
    return  HttpResponse(content)



def index(request):
    pass

@check_token
def turn_on_blog(requets, *args, **kwargs):
    playload = args[0]
    username = playload["name"]

    blog = Blog.objects.filter(username=username)
    if blog:
        pass
    blog_name = username +"`s blog"
    Blog.objects.create(name=blog_name)