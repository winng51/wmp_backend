from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

import json
from wmp_backend.settings import APP_ID, APP_KEY, MEDIA_ROOT
from .models import Label, Topic, Picture, Comment, SubComment, User

import urllib
import requests
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler


def get_image(src, name):
    image = urllib.request.urlretrieve(src)
    img_temp = SimpleUploadedFile(name + '.jpg', open(image[0], "rb").read())

    return File(img_temp)


def open_id_login(request):
    if request.method == 'POST':
        code = request.POST['code']
        print(request.POST['userName'])
        if not code:
            response = json.dumps({'message': '缺少code'}, cls=DjangoJSONEncoder)
            return HttpResponse(response, content_type="application/json", status_code=400)

        url = "https://api.weixin.qq.com/sns/jscode2session?appid=" \
              "{0}&secret={1}&js_code={2}&grant_type=authorization_code".format(APP_ID, APP_KEY, code)
        wechat_response = json.loads(requests.get(url).content)  # 将json数据包转成字典
        openid = wechat_response['openid'] if 'openid' in wechat_response else None
        # session_key = res['session_key'] if 'session_key' in res else None
        if not openid:
            if 'errcode' in wechat_response:
                print(wechat_response['errcode'])
                response = json.dumps({'message': '微信调用失败', 'errcode': wechat_response['errcode']},
                                      cls=DjangoJSONEncoder)
            else:
                response = json.dumps({'message': '微信调用失败'}, cls=DjangoJSONEncoder)
            return HttpResponse(response, status=503)
        # 判断用户是否第一次登录
        try:
            user = User.objects.get(openid=openid)
        except User.DoesNotExist:
            # 微信用户第一次登陆,新建用户
            username = request.POST['username']
            gender = request.POST['gender']
            avatar = get_image(request.POST['avatar'], username)
            print(username, gender, avatar)
            user = User.objects.create(username=username, gender=gender, avatar=avatar, openid=openid, authority=0)

        # 手动签发jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response_data = {
            "userId": user.id,
            "token": token,
            "userName": user.username,
            "gender": user.gender,
            "avatar": 'https://wmp.winng51.cn/static/' + str(user.avatar),
        }
        print(response_data)

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def identity(request):
    if request.method == 'POST':
        token = request.POST['token']
        try:
            user_info = jwt_decode_handler(token)
        except ValueError:
            print(token)
            response = json.dumps(token, cls=DjangoJSONEncoder)
            return HttpResponse(response, content_type="application/json")

        try:
            user = User.objects.get(id=user_info['user_id'])
        except User.DoesNotExist:
            response = json.dumps({'message': '未登录'}, cls=DjangoJSONEncoder)
            return HttpResponse(response, content_type="application/json", status_code=400)

        user.gender = request.POST['gender']
        user.avatar = get_image(request.POST['avatarUrl'], request.POST['username'])
        user.username = request.POST['username']
        user.name = request.POST['name']
        user.college = request.POST['college']
        user.grade = request.POST['grade']
        user.classes = request.POST['class']
        user.phone = request.POST['mobile']
        user.identity = True
        user.save()

        response_data = {
            "userName": user.username,
            "gender": user.gender,
            "avatar": 'https://wmp.winng51.cn/static/' + str(user.avatar),
        }

        response = json.dumps(response_data, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")


def get_authority(request):
    if request.method == 'POST':
        token = request.POST['token']
        user_info = jwt_decode_handler(token)
        user_authority = User.objects.get(id=user_info['user_id']).authority
        response = json.dumps(user_authority, cls=DjangoJSONEncoder)
        return HttpResponse(response, content_type="application/json")
