import datetime
import json
import logging

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from blog.models import Blog
from common.views import *
from userinfo.models import UserInfo, Contact

# token有效时间
timedelta = datetime.timedelta(seconds=1000).total_seconds()

# 注册
class RegisterView(View):
    def get(self, request, *args, **kwagrs):
        return render(request, "userinfo/register.html")

    def post(self, request, *args, **kwargs):
        # print(request.META.get("HTTP_REFERER"))
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("username:", username, "password:", password)
        # 数据校验
        user = UserInfo.objects.filter(username=username)
        if user:
            dic = {
                "action": "register",
                "success": False,
                "message": "用户名已存在",
            }
            json_str = json.dumps(dic)
            response = HttpResponse(json_str)
            return response

        # 数据校验通过，创建用户
        if username and password:
            user = UserInfo.objects.create(username=username, password=make_password(password, None, "pbkdf2_sha256"))

            print("user:", user)
            dic = {
                "action": "register",
                "success": True,
                "message": "注册成功",
            }

            # 注册的同时开通博客
            Blog.objects.create(user=user, name=user.username + " of blog")

            response = JsonResponse(dic)
            return response

        dic = {
            "action": "register",
            "success": False,
            "message": "用户名或密码不能为空",
        }
        json_str = json.dumps(dic)
        # 数据校验不通过，返回
        return HttpResponse(json_str)

# 登录
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "userinfo/login.html",)

    def post(self, request, *args, **kwargs):

        dic = {
            "is_login": False,
            "username": "anonymous",
            "access_token": "",
            "message": "您的输入有误",
        }

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = UserInfo.objects.filter(username=username)
        if not user:
            responese = JsonResponse(dic)
            responese.status_code = 404

            return responese

        password_ = user[0].password
        pwd = check_password(password, password_, None, "pbkdf2_sha256")

        if user and pwd:
            user[0].save()
            last_login = user[0].last_login.timestamp()

            header_payload = dinfine_header_payload(user[0].id,username, timedelta, last_login)
            access_token = create_access_token(**header_payload)
            dic.update({"is_login": True, "username": username, "access_token": access_token, "message": "登录成功"})

            responese = JsonResponse(dic)

            return responese

        responese = JsonResponse(dic)
        responese.status_code = 404
        return responese


# class UserInfoView(View):
#     @method_decorator(check_access_token)
#     def get(self, request, payload, *args, **kwargs):
#         new_token = refresh_access_token(*args, **kwargs)
#         user = UserInfo.objects.filter(username=payload["name"])[0]
#         dic = {
#             "data": {"name": user.username, "sex": user.sex},
#             "new_token": new_token,
#         }
#         json_str = json.dumps(dic)
#
#         return HttpResponse(json_str)


class IsVailTokenView(View):
    @method_decorator(check_access_token)
    def get(self, request, payload, *args, **kwargs):

        # 自动刷新access_token
        new_acces_token = refresh_access_token(payload)
        print("payload:", payload)
        username =payload["name"]
        dic = {
            "is_login": True,
            "username": username,
            "new_access_token": new_acces_token,
            "message": "登录成功",
        }

        return JsonResponse(dic)
        # json_str = json.dumps(dic)
        # return HttpResponse(json_str)


# 关注,be_folowed为被关注的人
class ContactView(View):
    @method_decorator(check_access_token)
    def post(self, request, playload, username, action, be_followed,  *args, **kwargs):
        if username == be_followed:
                dic = {
                    "success": False,
                    "display": "关注",
                    "messages": "you can't contact yourself",
                }
                response = JsonResponse(dic)
                response.status_code = 404
                return JsonResponse(dic)

        user_from = get_object_or_404(UserInfo, username=username)
        user_to = get_object_or_404(UserInfo, username=be_followed)
        contact = Contact.objects.filter(user_from=user_from, user_to=user_to, is_active=True)

        # print(username)
        if action == "is_contacted":
            if contact:
                dic = {
                    "success": True,
                    "display": "已关注",
                    "messages": "have been contacted",
                }
                return JsonResponse(dic)
            else:
                dic = {
                    "success": True,
                    "display": "关注",
                    "messages": "is not contacted",
                }
                return JsonResponse(dic)
        elif action == "follow":
            Contact.objects.update_or_create(user_from=user_from, user_to=user_to, defaults={"is_active": True})
            dic = {
                "success": True,
                "display": "已关注",
                "messages": "contact successfull",
            }
            return JsonResponse(dic)
        elif action == "cancel":
            Contact.objects.filter(user_from=user_from, user_to=user_to).update(is_active=False)
            dic = {
                "success": True,
                "display": "关注",
                "messages": "cancel successfull",
            }

            return JsonResponse(dic)

        dic = {
            "success": False,
            "display": "关注",
            "messages": "can't understand you meaning",
        }

        response = JsonResponse(dic)
        response.status_code = 404
        return response
