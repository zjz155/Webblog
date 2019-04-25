import base64
import datetime
import hmac
import json

from django.conf.global_settings import PASSWORD_HASHERS
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import Webblog.settings
from userinfo.models import UserInfo

timedelta = datetime.timedelta(seconds=60).total_seconds()

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

        token = create_token(username, last_login)
        dic = {
            "action": "login",
            "username": username,
            "success": True,
            "token": token,
        }
        json_str = json.dumps(dic)

        return HttpResponse(json_str)

    return HttpResponse("用户名或密码不正确")

# 计算token
def create_token(username, last_login):

    exp = last_login + timedelta
    header = {
        "alg": "sha256",
        "typ": "JWT"
    }

    payload = {
        "sub": "1234567890",
        "exp": exp,
        "last_login": last_login,
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

    return token

# 判断token是否过期
def is_expire(exp):
    now = datetime.datetime.now().timestamp()
    if (exp - now) < 0.0:
        return True
    else:
        return False

# 计算新的token
def refresh_token(username, last_login):
    online_time = datetime.datetime.now().timestamp() - last_login
    print(online_time)
    print("old_last_login:", datetime.datetime.fromtimestamp(last_login))
    if online_time > timedelta / 2:
        user = UserInfo.objects.filter(username=username)
        last_login_ = user[0].last_login.timestamp()
        # 如果没有用新的token,返回None.
        if last_login != last_login_:
            return None

        user[0].save()
        last_login = user[0].last_login.timestamp()
        print("new_last_login:", datetime.datetime.fromtimestamp(last_login))
        return create_token(username, last_login)

    return None

# 验证token签名
def check_token(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
        jwt = token.split(".")
        header = jwt[0]
        payload = jwt[1]
        signature = jwt[2]

        # 解码后得到bytes格式
        header_ = base64.urlsafe_b64decode(header)
        # 解码成python字串符
        header_ = header_.decode()
        # print(header_)
        payload_ = base64.urlsafe_b64decode(payload)
        payload_ = payload_.decode()

        payload_dict = json.loads(payload_)
        header_dict = json.loads(header_)
        alg = header_dict["alg"]
        exp = payload_dict["exp"]
        username = payload_dict["name"]
        last_login = payload_dict["last_login"]

        s = header + "." + payload
        key = Webblog.settings.SECRET_KEY.encode()
        signature_ = hmac.new(key, s.encode(), alg).hexdigest()

        # 验证签名
        flag = hmac.compare_digest(signature_, signature)

        # 如果 验证签名失败或过期要求重新登入　
        if not flag or is_expire(exp) :
            dic = {
                "action": "check token",
                "success": False,
                "message": "请重新登寻...",
            }
            json_str = json.dumps(dic)
            return HttpResponse(json_str)

        return func(request, username, last_login)

    return wrapper

    # return HttpResponse("ok")


@check_token
def source(request,  *args, **kwargs):
    new_token = refresh_token(*args, **kwargs)
    dic = {
        "data": "你要的数据",
        "new_token": new_token,
    }
    json_str = json.dumps(dic)

    return HttpResponse(json_str)