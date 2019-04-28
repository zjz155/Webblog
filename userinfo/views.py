import datetime
import json
import logging

from django.conf.global_settings import PASSWORD_HASHERS
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from common.views import *
from userinfo.models import UserInfo

# Get an instance of a logger
logger = logging.getLogger("django")

timedelta = datetime.timedelta(seconds=60).total_seconds()

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

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
        return HttpResponse("OK")

    dic = {
        "action": "register",
        "success": False,
        "message": "用户名或密码不能为空",
    }
    json_str = json.dumps(dic)
    # 数据校验不通过，返回
    return HttpResponse(json_str)

# 登录
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    password_ = UserInfo.objects.filter(username=username)[0].password

    user = UserInfo.objects.filter(username=username)
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


@check_token
def userinfo(request,  *args, **kwargs):
    new_token = refresh_token(*args, **kwargs)
    payload = args[0]
    print()
    user = UserInfo.objects.filter(username=payload["name"])[0]
    dic = {
        "data": {"name": user.username, "sex": user.sex},
        "new_token": new_token,
    }
    json_str = json.dumps(dic)

    return HttpResponse(json_str)