import base64
import hmac
import json

from django.conf.global_settings import PASSWORD_HASHERS
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import Webblog.settings
from userinfo.models import UserInfo

def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    # 数据校验
    user = UserInfo.objects.filter(username=username)
    if user:
        dic = {
            "error": 400,
            "message": "用户名已存在"
        }
        json_str = json.dumps(dic)
        response = HttpResponse(json_str)
        return response

    # 数据校验通过，创建用户
    if username and password:
        UserInfo.objects.create(username=username, password=make_password(password, None, "pbkdf2_sha256"))
        return HttpResponse("OK")

    dic = {
        "error": 400,
        "message": "用户名或密码不能为空"
    }
    json_str = json.dumps(dic)
    # 数据校验不通过，返回
    return HttpResponse(json_str)


def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    password_ = UserInfo.objects.filter(username=username)[0].password

    user = UserInfo.objects.filter(username=username)
    pwd = check_password(password, password_, None, "pbkdf2_sha256")


    if user and pwd:
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
        "admin": False,
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

    # 指定一个密钥（secret）https://docs.python.org/3/library/secrets.html?highlight=choice#module-secrets
    key = Webblog.settings.SECRET_KEY.encode()

    # 对前两部分 s 的签名
    signature = hmac.new(key, s.encode(), "sha256").hexdigest()
    # 把 Header、Payload、Signature 三个部分拼成一个字符串，每个部分之间用"点"（.）分隔
    token = s + "." + signature

    return HttpResponse(token)


def check_jwt(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        jwt = token.split(".")
        header = jwt[0]
        payload = jwt[1]
        signature = jwt[2]
        # 解码后得到bytes格式
        header_ = base64.urlsafe_b64decode(header)
        # 解码成python字串符
        header_ = header_ .decode()
        # print(header_)

        header_dict = json.loads(header_)
        alg = header_dict["alg"]
        s = header + "." + payload
        key = Webblog.settings.SECRET_KEY.encode()

        signature_ = hmac.new(key, s.encode(), alg).hexdigest()

        # 验证签名
        flag = hmac.compare_digest(signature_, signature)
        # flag = 0
        if flag:
            # print("signature：", signature, "header:", type(header_dict), "flag:", flag)
            return func(request, *args, **kwargs)

        else:
            return HttpResponse("你错了。。。")

    return wrapper

    # return HttpResponse("ok")


@check_jwt
def source(request):
    return HttpResponse("你找到我了。。。。")
