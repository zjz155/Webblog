import datetime
import json
import logging

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from common.views import *
from userinfo.models import UserInfo, Contact

# Get an instance of a logger
# logger = logging.getLogger("django")

# token有效时间
timedelta = datetime.timedelta(seconds=60*60).total_seconds()

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
            UserInfo.objects.create(username=username, password=make_password(password, None, "pbkdf2_sha256"))
            dic = {
                "action": "register",
                "success": True,
                "message": "注册成功",
            }
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
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = UserInfo.objects.filter(username=username)
        if not user:
            return HttpResponse("用户名不存在")

        password_ = user[0].password
        pwd = check_password(password, password_, None, "pbkdf2_sha256")

        if user and pwd:
            user[0].save()
            last_login = user[0].last_login.timestamp()

            header_payload = dinfine_header_payload(username, timedelta, last_login)
            token = create_token(**header_payload)

            dic = {
                "action": "login",
                "username": username,
                "success": True,
                "token": token,
                "message": "登录成功",
            }
            json_str = json.dumps(dic)

            return HttpResponse(json_str)

        return HttpResponse("用户名或密码不正确")


class UserInfoView(View):
    @method_decorator(check_token)
    def get(self, request, *args, **kwargs):
        new_token = refresh_token(*args, **kwargs)
        payload = args[0]
        user = UserInfo.objects.filter(username=payload["name"])[0]
        dic = {
            "data": {"name": user.username, "sex": user.sex},
            "new_token": new_token,
        }
        json_str = json.dumps(dic)

        return HttpResponse(json_str)


class IsVailTokenView(View):
    @method_decorator(check_token)
    def get(self, request, *args, **kwargs):
        payload = args[0]
        print("*args:", *args)
        username =payload["name"]
        dic = {
            "action": "login",
            "username": username,
            "success": True,
            "token": "",
            "message": "登录成功",
        }

        return JsonResponse(dic)
        # json_str = json.dumps(dic)
        # return HttpResponse(json_str)


# 关注,be_folowed为被关注的人
class ContactView(View):
    def post(self, follower, action, be_folowed,  *args, **kwargs):
        if action == "follow":
            Contact.objects.update_or_create(user_from=follower, user_to=be_folowed, defaults={"is_active": True})
            dic = {
                "success": True,
                "messages": "contact successfull"
            }
            return JsonResponse(dic)
        else:
            Contact.objects.filter(user_from=follower, user_to=be_folowed).upadte(is_active=False)
            dic = {
                "success": True,
                "messages": "cancel successfull"
            }

            return JsonResponse(dic)