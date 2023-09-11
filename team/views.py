import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from django.core.exceptions import ObjectDoesNotExist
from tools.user_dec import *
import base64
import hashlib
import time
import random

from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, user_logged_in, user_logged_out
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import jwt
from django.conf import settings

# from tools.user_dec import check_token
from user.models import *
from django.conf import settings


def add_team_member(request, username):  # 添加团队成员
    if request.method == 'POST':
        try:
            json_str = request.body.decode()
            data = json.loads(json_str)
            teamname = data['teamname']
            newname = data['username']
            team = Team.objects.get(teamname=teamname)
            user = User.objects.get(username=username)
            newuser = User.objects.get(username=newname)
            leader = TeamMember.objects.get(userid=user, teamid=team)
            if leader.role > 0:
                existing_member = TeamMember.objects.filter(userid=newuser, teamid=team)
                if existing_member.exists():
                    return JsonResponse({'code': 10011, 'error': '团队成员已存在'})
                TeamMember.objects.create(userid=newuser, teamid=team, role=0)
                UserToTeam.objects.create(userid=newuser.userid, teamid=team.teamid)
                TeamToUser.objects.create(userid=newuser.userid, teamid=team.teamid)
                return JsonResponse({'code': 200, 'message': '团队成员添加成功'})
            else:
                return JsonResponse({'code': 10010, 'error': '用户权限不够'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'code': 400, 'error': '只支持POST请求'})


def delete_team_member(request, username):  # 删除团队成员
    if request.method == 'POST':
        try:
            json_str = request.body.decode()
            data = json.loads(json_str)
            teamname = data['teamname']
            deletename = data['deletename']
            team = Team.objects.get(teamname=teamname)
            user = User.objects.get(username=username)
            leader = TeamMember.objects.get(userid=user, teamid=team)
            deleteuser = User.objects.get(username=deletename)
            deletemember = TeamMember.objects.get(teamid=team, userid=deleteuser)
            if leader.role > 0 and deletemember.role == 0:
                deletemember.delete()
                deleterelate1 = UserToTeam.objects.get(userid=newuser.userid, teamid=team.teamid)
                deleterelate2 = TeamToUser.objects.get(userid=newuser.userid, teamid=team.teamid)
                deleterelate1.delete()
                deleterelate2.delete()
                return JsonResponse({'code': 200, 'message': '团队成员删除成功'})
            else:
                return JsonResponse({'code': 10010, 'error': '用户权限不够'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'code': 400, 'error': '只支持POST请求'})


def add_admin(request, username):  # 添加团队管理员
    if request.method == 'POST':
        try:
            json_str = request.body.decode()
            data = json.loads(json_str)
            teamname = data['teamname']
            adminname = data['username']
            team = Team.objects.get(teamname=teamname)
            user = User.objects.get(username=username)
            admin = User.objects.get(username=adminname)
            leader = TeamMember.objects.get(userid=user, teamid=team)
            adminmember = TeamMember.objects.get(teamid=team, userid=admin)
            if leader.role >= 1 and adminmember.role == 0:
                adminmember.role = 1
                adminmember.save()
                return JsonResponse({'code': 200, 'message': '管理员设置成功'})
            else:
                return JsonResponse({'code': 10010, 'error': '用户权限不够,或者该用户已经是管理员'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'code': 400, 'error': '只支持POST请求'})


def delete_admin(request, username):  # 删除团队管理员
    if request.method == 'POST':
        try:
            json_str = request.body.decode()
            data = json.loads(json_str)
            teamname = data['teamname']
            adminname = data['username']
            team = Team.objects.get(teamname=teamname)
            user = User.objects.get(username=username)
            admin = User.objects.get(username=adminname)
            leader = TeamMember.objects.get(userid=user, teamid=team)
            adminmember = TeamMember.objects.get(teamid=team, userid=admin)
            if leader.role > 1 and adminmember.role == 1:
                adminmember.role = 0
                return JsonResponse({'code': 200, 'message': '管理员删除成功'})
            else:
                return JsonResponse({'code': 10010, 'error': '用户权限不够'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    else:
        return JsonResponse({'code': 400, 'error': '只支持POST请求'})


def get_teamid_list_simple(userid):
    return [x.teamid for x in UserToTeam.objects.filter(userid=userid)]


# 获取team列表的详情(具体信息)
def get_team_list_detail(userid):
    return [Team.objects.get(teamid=x).to_dic() for x in get_teamid_list_simple(userid)]


def get_memberid_list_simple(teamid):
    return [x.userid for x in TeamToUser.objects.filter(teamid=teamid)]


# 获取team成员列表的详情(具体信息)
def get_member_list_detail(teamid):
    return [User.objects.get(userid=x).to_dic() for x in get_memberid_list_simple(teamid)]



def get_team_list(request,username):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            result = {'result': 0, 'message': r"请先登录!"}
            return JsonResponse(result)

        result = {'result': 1, 'message': r"获取团队列表成功！", "user": user.to_dic(),
                  "like_list": get_team_list_detail(user.userid)}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"发生错误！"}
        return JsonResponse(result)


def get_user_list(request, teamname):
    if request.method == 'POST':
        try:
            team = Team.objects.get(teamname=teamname)
        except Exception as e:
            result = {'result': 0, 'message': r"请先登录!"}
            return JsonResponse(result)

        result = {'result': 1, 'message': r"获取团队成员列表成功！", "user": team.to_dic(),
                  "like_list": get_member_list_detail(team.teamid)}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"发生错误！"}
        return JsonResponse(result)
