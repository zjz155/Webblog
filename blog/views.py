import json

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import *
from common.views import check_token, refresh_token
from userinfo.models import UserInfo

class GrantBlogView(View):
    @method_decorator(check_token)
    def post(self, request, *args, **kwargs):
        new_token = refresh_token(*args, **kwargs)
        payload = args[0]
        user = UserInfo.objects.filter(username=payload["name"])[0]

        blog = Blog.objects.filter(user=user)
        if blog:
            return HttpResponse("博客已存在")

        Blog.objects.create(user=user, name=user.username + " of blog")

        return HttpResponse("成功开通博客")

@method_decorator(check_token, name="dispatch")
class CompileBlogEntry(View):
    def get(self, request, *args, **kwargs):
        return render(request, "markdown.html")

    def post(self, request, *args, **kwargs):
        payload = args[0]
        user = UserInfo.objects.filter(username=payload["name"])

        blog = Blog.objects.filter(user=user[0])
        headline = request.POST["headline"]
        content = request.POST["content"]
        Entry.objects.update_or_create(blog=blog[0], headline=headline,  defaults={"body_text":content})
        print(content)

        return HttpResponse("保存成功")

class TestView(View):
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        return  HttpResponse("haha")

@check_token
def write_blog_entry(request, *args, **kwargs):
    if request.method == "GET":
        return render(request, "markdown.html")

    user = UserInfo.objects.filter(username="jz-zhou")
    blog = Blog.objects.filter(user=user[0])
    content = request.POST["content"]
    Entry.objects.create(blog=blog[0], headline="2019-04-24 17:49:17django 视图装饰器（View decorators）", body_text=content)


    print(content)

    return HttpResponse("ok")


class DetialEntryView(View):
    def get(self, request, username, article_id, *args, **kwargs):
        return render(request, "read_markdown.html", context={"username": username, "article_id": article_id})

class ListEntryView(View):
    def get(self, request, username, *args, **kwargs):
        return render(request, "read_markdown.html", context={"username": username})

def read(request, usesrname, id, ):
    return render(request, "read_markdown.html")


def read_blog_entry(request, username, article_id, *agrs, **kwargs):
    entry = get_object_or_404(Entry, id=article_id)
    content = entry.body_text
    return  HttpResponse(content)

def indexview(request):
    return render(request, "index.html")

def index(request,*args, **kwargs):
    entry_list = Entry.objects.all().order_by("-pub_date")
    paginator = Paginator(entry_list, 5)
    count = paginator.count
    page_num = paginator.num_pages

    # page = request.GET.get('page')
    page = 1
    entries_page = paginator.get_page(1)
    has_next = entries_page.has_next()
    has_previous = entries_page.has_previous()

    entries_object_list = entries_page.object_list

    entries = [{"headline": obj.headline, "abstract": obj.abstract, "pub_date": obj.pub_date.strftime("%Y-%m-%d"),
                "blog": obj.blog.name, "link":obj.get_absolute_url()} for obj in entries_object_list]

    dic = {
        "page":{
            "has_next": has_next,
            "has_previous": has_previous,
            "page_num": page_num,
        },

        "entries":entries

    }
    json_str = json.dumps(dic)
    print(entries)
    response = HttpResponse(json_str)

    return response

@check_token
def turn_on_blog(requets, *args, **kwargs):
    playload = args[0]
    username = playload["name"]

    blog = Blog.objects.filter(username=username)
    if blog:
        pass
    blog_name = username +"`s blog"
    Blog.objects.create(name=blog_name)