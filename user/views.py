import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from tools.user_dec import *
from .models import User
import base64
import hashlib
import time
import random

from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse

# from tools.sms import YunTongXin
# Create your views here.
from django.contrib.auth import authenticate, user_logged_in, user_logged_out
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt
from django.conf import settings

# from tools.user_dec import check_token
from .models import *
from django.conf import settings


def register(request):
    try:
        json_str = request.body
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        result = {'code': 10112, 'error': 'Invalid JSON data'}
        return JsonResponse(result)
    username = json_obj['username']
    # nickname = json_obj['nickname']
    email = json_obj['email']
    password_1 = json_obj['password']
    password_2 = json_obj['repassword']
    # telephone = json_obj['telephone']
    sms_num = json_obj['sms_num']
    if password_1 != password_2:
        result = {'code': 10100, 'error': 'The password is not same'}
        return JsonResponse(result)

    old_code = cache.get('sms_%s' % email)
    if not old_code:
        result = {'code': '10110', 'error': 'The code is wrong'}
        return JsonResponse(result)
    if int(sms_num) != old_code:
        result = {'code': '10111', 'error': 'The code is wrong'}
        return JsonResponse(result)

    # 用户名是否可用
    old_users = User.objects.filter(username=username)
    if old_users:
        result = {'code': 10101, 'error': 'The username is already existed'}
        return JsonResponse(result)
    p_m = hashlib.md5()
    p_m.update(password_1.encode())
    User.objects.create(username=username, password=p_m.hexdigest(), email=email, )  # avatar='default.png',)

    # 参数的基本检查：密码不能超过多少位，用户名是否可用
    # 异常返回：
    # result = {'code':10100,'error':'The username is already existed'}
    # return JsonResponse(result)
    # 异常码范围：10100 - 10199
    result = {'code': 200, 'username': username}
    return JsonResponse(result)


def login(request):
    if request.method == 'POST':
        json_str = request.body.decode()
        # print(json_str)
        data = json.loads(json_str)
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'code': 10201, 'error': '用户不存在'}
            return JsonResponse(result)

        p_m = hashlib.md5()
        p_m.update(password.encode())
        hashed_password = p_m.hexdigest()
        if user.password != hashed_password:
            result = {'code': 10202, 'error': '输入密码错误'}
            return JsonResponse(result)

        user.save()
        # 用户验证成功，生成JWT令牌
        key = settings.JWT_TOKEN_KEY
        now_time = time.time()
        payload = {'username': username}
        token = jwt.encode(payload, key, algorithm='HS256')
        result = {'code': 200, 'username': username}
        user_logged_in.send(sender=None, user=user, request=request)
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)


def send_email(recipient_email, message):
    # 你的邮箱登录信息
    sender_email = '3361700030@qq.com'
    sender_password = 'aguhhvynvqkudbeb'

    # 构建邮件内容
    subject = '验证码'
    body = message
    message = MIMEText(str(message), 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email

    try:
        # 连接到 SMTP 服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # server.starttls()
        server.login(sender_email, sender_password)

        # 发送邮件
        server.sendmail(sender_email, [recipient_email], message.as_string())

        # 关闭连接
        server.quit()
        # 邮件发送成功
        return True
    except Exception as e:
        # 邮件发送失败
        error_msg = str(e)
        print(f'邮件发送失败：{error_msg}')
        return error_msg


def sms_view(request):
    if request.method != 'POST':
        result = {'code': 10108, 'error': 'Please use POST'}
        return JsonResponse(result)
    json_str = request.body
    json_obj = json.loads(json_str)
    email = json_obj['email']
    # 生成随机码
    code = random.randint(1000, 9999)
    print('email', email, ' code', code)
    # 存储随机码 django-redis sudo pip3 install django-redis
    cache_key = 'sms_%s' % email
    # 检查是否已经有发过的且未过期的验证码
    old_code = cache.get(cache_key)
    if old_code:
        return JsonResponse({'code': 10111, 'error': 'The code is already existed'})

    cache.set(cache_key, code, 60)
    # 发送随机码 -> 短信
    send_result = send_email(email, code)
    if send_result is True:
        return JsonResponse({'code': 200})
    else:
        error_msg = f'邮件发送失败：{send_result}'
        return JsonResponse({'code': 10112, 'error': error_msg})


def find_password(request, username):
    if request.method == 'POST':
        json_str = request.body.decode()
        data = json.loads(json_str)
        email = data['email']
        sms_num = data['sms_num']
        user = User.objects.get(username=username)

        old_code = cache.get('sms_%s' % (email))
        if not old_code:
            result = {'code': '10203', 'error': '验证码错误'}
            return JsonResponse(result)
        if int(sms_num) != old_code:
            result = {'code': '10203', 'error': '验证码错误'}
            return JsonResponse(result)

        p_m = hashlib.md5()
        p_m.update(data['password'].encode())
        user.password = p_m.hexdigest()

        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)


def form_team(request, username):
    if request.method == 'POST':
        json_str = request.body.decode()
        data = json.loads(json_str)
        teamname = data['teamname']
        leader = User.objects.get(username=username)
        members = request.POST.getlist('members')  # 获取多个成员

        # 创建团队对象
        team = Team.objects.create(
            teamname=teamname,
            creatorid=leader,
        )
        TeamMember.objects.create(
            userid=leader,
            teamid=team,
            role=2,
        )
        TeamToUser.objects.create(
            userid=leader,
            teamid=team,
        )
        UserToTeam.objects.create(
            userid=leader,
            teamid=team,
        )
        valid_members = []
        # 添加成员
        for member_name in members:
            try:
                member = User.objects.get(username=member_name)
                valid_members.append(member)
            except User.DoesNotExist:
                pass  # 忽略不存在的成员
        for member in valid_members:
            TeamMember.objects.create(
                userid=member.userid,
                teamid=team.teamid,
                role=0,
            )
        public_chat = PublicChat.objects.create(teamid=team)
        for member in valid_members:
            PublicChatMember.objects.create(chatid=public_chat, userid=member.userid)
        return JsonResponse({'code': 200, 'message': '团队和群聊创建成功'})
    else:
        return JsonResponse({'code': 400, 'error': '只支持POST请求'})


def info(request, username):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'code': 10201, 'error': '用户不存在'}
            return JsonResponse(result)
        # 关注者数量
        # team_num = user.join.all().count()
        result = {'code': 200, 'username': username, 'data': {'nickname': user.nickname, 'email': user.email,
                                                              'birthday': user.birthday, 'sex': user.sex, 'location': user.location,
                                                              'signature': user.signature}}
        return JsonResponse(result)

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)
@check_token
def change_info(request,username):
    if request.method == 'PUT':
        json_str = request.body.decode()
        data = json.loads(json_str)

        user = request.myuser

        user.nickname = data['nickname']
        user.email = data['email']
        user.sex = data['sex']
        user.location = data['location']

        user.save()
        return JsonResponse({'code': 200})

    else:
        result = {'code': 10200, 'error': '请求方式错误'}
        return JsonResponse(result)
