import json
from datetime import datetime

from django.core.cache import caches
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import *
from common.views import check_access_token, refresh_access_token
from userinfo.models import UserInfo

# 首页,展示所有文章,按间降序
class IndexView(View):
    def get(self, request, username="jz_zhou", data= "list", *args, **kwargs):
        if data == "list":
            return render(request, "blog/blog.html")

        user = UserInfo.objects.get(username=username)

        entry_list = Entry.objects.filter(user=user).order_by("-pub_date")
        if not entry_list:
            dic = {
                "message": "not found entries",

            }
            response = JsonResponse(dic)
            response.status_code = 404
            return response

        paginator = Paginator(entry_list, 1)
        #　所有页的item的总和
        count = paginator.count
        # 一共有几页
        num_pages = paginator.num_pages

        # page = request.GET.get('page')
        # page = 1
        # 获取某页的对象
        entries_page = paginator.get_page(data)
        has_next = entries_page.has_next()
        has_previous = entries_page.has_previous()
        page_number= entries_page.number
        entries_object_list = entries_page.object_list

        print("blog:", UserInfo.objects.get(username = "jz_zhou").blog.name)

        entries = [{"headline": obj.headline, "abstract": obj.abstract, "pub_date": obj.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user": UserInfo.objects.get(username = obj.user.username).blog.name, "link": obj.get_absolute_url()} for obj in entries_object_list]

        dic = {
            "has_next": has_next,
            "has_previous": has_previous,
            "num_pages": num_pages,
            "page_number": page_number,
            "count": count,

            "entries": entries

        }
        json_str = json.dumps(dic)
        print(dic)
        response = HttpResponse(json_str)

        return response

# 开通博客功能
class GrantBlogView(View):
    @method_decorator(check_access_token)
    def post(self, request, payload, *args, **kwargs):
        new_token = refresh_access_token(*args, **kwargs)
        user = UserInfo.objects.filter(username=payload["name"])[0]

        blog = Blog.objects.filter(user=user)
        if blog:
            return HttpResponse("博客已存在")

        Blog.objects.create(user=user, name=user.username + " of blog")

        return HttpResponse("成功开通博客")


# 写博客
class CompileBlogEntry(View):
    def get(self, request, *args, **kwargs):
        return render(request, "blog/markdown.html")

    @method_decorator(check_access_token)
    def post(self, request, payload, *args, **kwargs):
        user = UserInfo.objects.filter(username=payload["name"])

        blog = Blog.objects.filter(blog=user[0])
        headline = request.POST["headline"]
        content = request.POST["content"]
        Entry.objects.update_or_create(user=user[0], headline=headline,  defaults={"body_text":content})
        print(headline)
        print(content)

        return HttpResponse("保存成功")

# 文章详情
class DetialEntryView(View):
    def get(self, request, username, article_id, *args, **kwargs):
        return render(request, "blog/read_markdown.html")


class ReadBlogEntry(View):
    def get(self, request, username, article_id, *args, **kwargs):
        entry_user = get_object_or_404(UserInfo, username=username)
        entry = get_object_or_404(Entry, id=article_id)
        headline = entry.headline
        content = entry.body_text
        entry.rating += 1
        dic = {
            "entry_user_id": entry_user.id,
            "article_id": article_id,
            "content": content,
            "headline": headline,
        }
        # content = entry.body_text
        return JsonResponse({"content": content, "headline": headline})


# 评论
class CommentView(View):
    def get(self, request, article_id, page=1, *args, **kwargs):
        comment_list = Comment.objects.all().order_by("-created")
        paginator = Paginator(comment_list, 5)
        page = paginator.get_page(page)
        has_next = page.has_next()
        obj_list = page.object_list

        comment = [{"entry_id": obj.entry.id, "username": obj.user.username, "comment": obj.body } for obj in obj_list]
        dic = {
            "has_next": has_next,
            "comment": comment,
        }

        return JsonResponse(dic)

    def post(self, request, article_id, blog_id, *args, **kwargs):
        comment = request.POST.get("comment", "")
        if comment:
            Comment.objects.create(entry=article_id, blog=blog_id)
            dic = {
                "success": True,
                "messsage": "comment successfull"
            }

            return JsonResponse(dic)

# 回复
class ReplyView(View):
    def get(self, request, article_id, page=1, *args, **kwargs):
        reply_list = Reply.objects.all().order_by("-created")
        paginator = Paginator(reply_list, 5)
        page = paginator.get_page(page)
        has_next = page.has_next()
        obj_list = page.object_list

        reply = [{"comment_id": obj.comment.id, "username": obj.user.username, "reply": obj.body} for obj in obj_list]
        dic = {
            "has_next": has_next,
            "reply": reply,
        }

        return JsonResponse(dic)

    def Post(self, request, comment_id, reply, *args, **kwargs):
        payload = args[0]
        username = payload["name"]
        user = UserInfo.objects.get(username=username)
        reply = request.POST.get("reply", "")
        Reply.objects.create(comment=comment_id, user=user, body=reply)

        dic = {
            "success": True,
            "message": "reply successfully"
        }

        return JsonResponse(dic)


class HotEntryView(View):
    def get(self, request, num, *args, **kwargs):
        hot_entry = Entry.objects.all().order_by("-rating")[num]

        dic = {
            "num": len(hot_entry),
            "hot_entry":[{"headline": obj.headline, "url": obj.get_absolute_url} for obj in hot_entry]
        }
        print("test")
        return JsonResponse(dic)


class TestView(View):
    def get(self, request, *args, **kwargs):
        cache = caches["default"]
        cache.set("mycache", "中国")
        print("cache.get:" , cache.get("testcache"))
        print(args, kwargs)
        return  HttpResponse("haha")
    def put(self, request, *args, **kwargs):

        return JsonResponse({"method": "PUT"})