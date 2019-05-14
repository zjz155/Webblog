import base64
import datetime
import hmac
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from Webblog import settings

from userinfo.models import UserInfo

# 定义JWT的header和payload
def dinfine_header_payload(username, timedelta, iat, admin=False, alg="sha256"):
    exp = iat + timedelta
    header = {
        "alg": alg,
        "typ": "JWT"
    }

    payload = {
        "sub": "Webblog",
        "exp": exp,
        "iat": iat,
        "name": username,
        "admin": admin,
    }

    return {"header": header, "payload": payload}

# 计算token
def create_token(header={"alg": "sha256", "typ": "JWT"}, payload={"name": "anonymous", "sub": "subject"}):

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
    key = settings.SECRET_KEY.encode()

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
def refresh_token(payload):
    iat = payload["iat"]
    username = payload["name"]
    timedelta = payload["exp"] - iat

    online_time = datetime.datetime.now().timestamp() - iat
    print(online_time)
    print("old_iat:", datetime.datetime.fromtimestamp(iat))
    if online_time > timedelta / 2:
        user = UserInfo.objects.filter(username=username)
        iat_ = user[0].iat.timestamp()
        # 如果没有用新的token,返回None.
        if iat != iat_:
            return None

        user[0].save()
        iat = user[0].iat.timestamp()
        print("new_iat:", datetime.datetime.fromtimestamp(iat))
        header_payload = dinfine_header_payload(username, timedelta, iat)
        return create_token(**header_payload)

    return None

# 验证token签名
def check_token(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        if not token:
            dic = {
                "action": "check token",
                "success": False,
                "message": "请重新登寻...",
            }
            return JsonResponse(dic)
        token = token.split(" ")[1]
        jwt = token.split(".")
        try:
            header_jwt = jwt[0]
            payload_jwt= jwt[1]
            signature_jwt = jwt[2]
        except IndexError:
            dic = {
                "action": "check token",
                "success": False,
                "message": "请重新登寻...",
            }
            return JsonResponse(dic)

        # 解码后得到bytes格式
        header_ = base64.urlsafe_b64decode(header_jwt)
        # 解码成python字串符
        header_ = header_.decode()
        # print(header_)
        payload_ = base64.urlsafe_b64decode(payload_jwt)
        payload_ = payload_.decode()

        payload = json.loads(payload_)
        header = json.loads(header_)
        alg = header["alg"]
        exp = payload["exp"]

        s = header_jwt + "." + payload_jwt
        key = settings.SECRET_KEY.encode()
        signature_ = hmac.new(key, s.encode(), alg).hexdigest()

        # 验证签名
        flag = hmac.compare_digest(signature_, signature_jwt)


        # 如果 验证签名失败或过期要求重新登入　
        if not flag or is_expire(exp) :
            dic = {
                "action": "check token",
                "success": False,
                "message": "请重新登寻...",
            }
            json_str = json.dumps(dic)
            return HttpResponse(json_str)

        return func(request, payload)

    return wrapper

    # return HttpResponse("ok")