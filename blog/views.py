import json


from django.core.cache import caches
from django.core.paginator import Paginator
from django.db.models import Sum, F, Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import *
from common.views import check_access_token, htmlencode
from userinfo.models import UserInfo

# 首页,展示所有文章,按间降序
class IndexView(View):
    def get(self, request, username="jz_zhou", data="list", *args, **kwargs):
        if data == "list":
            return render(request, "blog/blog.html")

        # user = UserInfo.objects.get(username=username)
        user = get_object_or_404(UserInfo, username=username)
        search_title = request.GET.get("title", "")
        category = request.GET.get("category", "")
        print(category)
        if category:
            category = get_object_or_404(Category, category=category)
            entry_list = Entry.objects.filter(user=user, category=category).order_by("-pub_date")
        elif search_title:
            entry_list = Entry.objects.filter(user=user, headline__icontains=search_title).order_by("-pub_date")

        else:
            entry_list = Entry.objects.filter(user=user).order_by("-pub_date")

        categories = Category.objects.filter(entry__user=user).values("category").annotate(Count("category"))
        print("categories:", categories)
        if not entry_list:
            dic = {
                "message": "not found entries",
            }
            response = JsonResponse(dic)
            response.status_code = 404
            return response

        paginator = Paginator(entry_list, 2)
        # 所有页的item的总和
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

        print("blog:", UserInfo.objects.get(username="jz_zhou").blog.name)

        entries = [{"headline": obj.headline, "abstract": obj.abstract,
                    "pub_date": obj.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user": UserInfo.objects.get(username=obj.user.username).blog.name,
                    "pv": obj.pv,
                    "comments": obj.n_comments,
                    "link": obj.get_absolute_url()} for obj in entries_object_list]

        dic = {
            "has_next": has_next,
            "has_previous": has_previous,
            "num_pages": num_pages,
            "page_number": page_number,
            "count": count,

            "entries": entries,
            "categories": [{"category": d["category"],
                            "category__count": d["category__count"],
                            "rel": reverse("entry-list", args=[username, data]),
                            "href": reverse("entry-list", args=[username, "list"]) + "?category=" + d["category"],
                            }
                           for d in categories],

        }
        json_str = json.dumps(dic)
        print(dic)
        response = HttpResponse(json_str)

        return response

class BlogInfo(View):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(UserInfo, username=username)

        n_commets = Comment.objects.filter(entry__user=user).count()
        entries = Entry.objects.filter(user__username=username)
        pv = entries.aggregate(Sum("pv"))
        hots = entries.order_by("-pv")[:5]

        entries = [{"headline": obj.headline, "abstract": obj.abstract,
                    "pub_date": obj.pub_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "user": UserInfo.objects.get(username=obj.user.username).blog.name,
                    "pv": obj.pv,
                    "comments": obj.n_comments,
                    "link": obj.get_absolute_url()} for obj in hots]

        categories = Category.objects.filter(entry__user=user).values("category").annotate(Count("category"))

        dic = {
            "username": user.username,
            "blogname": user.blog.name,
            "n_comments": n_commets,
            "pv": pv["pv__sum"],
            "categories": [{"category": d["category"],
                            "n_categories": d["category__count"],
                            "rel": reverse("entry-list", args=[username, "list"]),
                            "href": reverse("entry-list", args=[username, "list"]) + "?category=" + d["category"],
                            }
                           for d in categories],
            "entry_hots": entries
        }
        response = JsonResponse(dic)
        return  response

# 开通博客功能
class GrantBlogView(View):
    @method_decorator(check_access_token)
    def post(self, request, payload, *args, **kwargs):


        blog = Blog.objects.filter(user_id=payload["id"])
        if blog:
            return HttpResponse("博客已存在")

        Blog.objects.create(user_id=payload["id"], name=payload["name"]+ " of blog")

        return HttpResponse("成功开通博客")


# 写博客
class CompileBlogEntry(View):
    def get(self, request, *args, **kwargs):
        return render(request, "blog/markdown.html")

    @method_decorator(check_access_token)
    def post(self, request, payload, *args, **kwargs):
        headline = request.POST["headline"]
        content = request.POST["content"]
        print("payload:",payload)
        Entry.objects.update_or_create(user_id=payload["id"], headline=headline,  defaults={"body_text":content})
        print(headline)
        print(content)

        return HttpResponse("保存成功")

# 文章详情
class DetialEntryView(View):
    def get(self, request, username, article_id, *args, **kwargs):
        return render(request, "blog/entry_detail.html")


class ReadBlogEntry(View):
    def get(self, request, username, article_id, *args, **kwargs):
        entry_user = get_object_or_404(UserInfo, username=username)
        entry_query = Entry.objects.filter(id=article_id)
        entry_query.update(pv=F("pv") + 1)
        headline = entry_query[0].headline
        content = entry_query[0].body_text

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
        comment_list = Comment.objects.filter(entry=article_id).order_by("-created")
        comment_paginator = Paginator(comment_list, 5)
        comment_page = comment_paginator.get_page(page)
        comment_has_next = comment_page.has_next()
        comment_obj_list = comment_page.object_list

        comment = [{"comment_info": {"comment_id": obj.id, "comment_username": obj.blog.name, "comment_content": obj.body, "comment_date": obj.created.strftime("%Y-%m-%d %H-%M-%S")},
                    "entry_info": {"entry_id": obj.entry.id, "entry_headline": obj.entry.headline, "entry_author": obj.entry.user.blog.name,},
                    "n_replys": obj.replys.count()} for obj in comment_obj_list]
        dic = {
            "has_next": comment_has_next,
            "comment_page": comment,
        }

        return JsonResponse(dic)

    @method_decorator(check_access_token)
    def post(self, request, payload, username, article_id, *args, **kwargs):
        blog = Blog.objects.get(user__username=username)
        print(args, kwargs)
        comment = htmlencode(request.POST["comment-content"])

#         comment = '''&lt;a&gt;xss&lt;/a&gt;
# &lt;scrtipt&gt;
# alert("xss")
# &lt;/scrtipt&gt;'''

        print(comment)
        if comment:
            Comment.objects.create(entry_id=article_id, blog=blog,  body=comment)
            Entry.objects.filter(id = article_id).update(n_comments=F('n_comments') + 1)

            dic = {
                "success": True,
                "messsage": "comment successfull"
            }

            return JsonResponse(dic)

        dic = {
            "success": False,
            "message": "comment fail, comment cant't be empty"
        }

        response = JsonResponse(dic)
        response.status_code = 404
        return response

# 回复
class ReplyView(View):
    def get(self, request, comment_id, page, *args, **kwargs):
        reply_list = Reply.objects.filter(comment=comment_id).order_by("-created")
        paginator = Paginator(reply_list, 20)
        page = paginator.get_page(page)
        has_next = page.has_next()
        obj_list = page.object_list

        reply = [{"comment_id": obj.comment.id, "reply_from": obj.reply_from.name, "reply_to": obj.reply_to.name, "reply_content": obj.body, "reply_time": obj.created } for obj in obj_list]
        dic = {
            "has_next": has_next,
            "reply": reply,
        }

        return JsonResponse(dic)

    @method_decorator(check_access_token)
    def post(self, request, payload, username, comment_id, *args, **kwargs):
        reply = htmlencode(request.POST["reply-content"])
        user = UserInfo.objects.get(username=username)
        reply_from = Blog.objects.get(user=user)
        commet = Comment.objects.get(id=comment_id)
        reply_to = Blog.objects.get(name=commet.blog.name)

        # reply = request.POST.get("reply", "")
        Reply.objects.create(comment=commet, reply_from=reply_from, reply_to=reply_to, body=reply)

        dic = {
            "success": True,
            "reply_from": reply_from.name,
            "reply_to": reply_to.name,
            "message": "reply successfully",
        }

        return JsonResponse(dic)


class HotEntryView(View):
    def get(self, request, num, *args, **kwargs):
        hot_entry = Entry.objects.all().order_by("-pv")[num]

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


