import base64
import hmac
import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import Webblog
from blog.models import UserInfo


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    # 数据校验

    # 数据校验通过，创建用户
    UserInfo.objects.create(username=username, password=password)
    # 数据校验不通过，返回

    return HttpResponse("OK")


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    flag = UserInfo.objects.filter(username=username, password=password)
    if flag:
        return jwt_views(username)

    return HttpResponse("用户名或密码不正确")


def jwt_views(username):
    header = {
        "alg": "sha256",
        "typ": "JWT"
    }

    payload = {
      "sub": "1234567890",
      "name": username,
      "admin": True
    }

    # 将header、payload字典对象变为字符串
    header_json_str = json.dumps(header)
    payload_json_str = json.dumps(payload)

    # 将header、payload字符串变为bytes字对象
    header_bytes = header_json_str.encode()
    payload_bytes = payload_json_str.encode()

    # 将header、payload进行base64编码
    header_jwt = base64.urlsafe_b64encode(header_bytes)
    payload_jwt = base64.urlsafe_b64encode(payload_bytes)

    # 将用　“." 将header和payload字符串连接起来
    s = header_jwt.decode() + "." + payload_jwt.decode()

    # 指定一个密钥（secret）
    key = Webblog.settings.SECRET_KEY.encode()

    # 对前两部分 s 的签名
    signature = hmac.new(key, s.encode(), "sha256").hexdigest()
    # 把 Header、Payload、Signature 三个部分拼成一个字符串，每个部分之间用"点"（.）分隔
    token = s + "." + signature

    return HttpResponse(token)


def check_jwt(func):
    def check(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        jwt = token.split(".")
        header = jwt[0]
        payload = jwt[1]
        signature = jwt[2]
        header_ = base64.urlsafe_b64decode(header)

        header_dict = json.loads(header_)
        alg = header_dict["alg"]
        s = header + "." + payload
        key = Webblog.settings.SECRET_KEY.encode()
        signature_ = hmac.new(key, s.encode(), alg).hexdigest()
        flag = hmac.compare_digest(signature_, signature)
        # flag = 0
        if flag:
            return func(request, *args, **kwargs)

            print("signature：", signature, "header:", type(header_dict), "flag:", flag)
        else:
            return HttpResponse("你错了。。。")

    return check

    # return HttpResponse("ok")


@check_jwt
def source(request):
    return HttpResponse("你找到我了。。。。")
