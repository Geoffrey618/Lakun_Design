import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from tools.user_dec import *
import base64
import hashlib
import time
import random
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
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


def create_project(request, username):  # 创建项目
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        projectname = json_obj['projectname']
        teamname = json_obj['teamname']

        team = get_object_or_404(Team, teamname=teamname)
        user = get_object_or_404(User, username=username)
        project = Project.objects.create(projectname=projectname, teamid=team, creatorid=user,
                                         created_time=timezone.now())
        TeamToProject.objects.create(teamid=team.teamid, projectid=project.projectid)
        # do more things

        result = {'result': 1, 'message': r"创建项目成功！", "project": project.to_dic()}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def get_project_list_simple(teamid):
    return [x.projectid for x in TeamToProject.objects.filter(teamid=teamid)]


def get_project_list_detail(teamid):
    return [Project.objects.get(projectid=x).to_dic() for x in get_project_list_simple(teamid)]


def get_project_detail(request):  # 查看项目详情
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        projectname = json_obj['projectname']

        teamname = json_obj['teamname']
        project = get_object_or_404(Project, projectname=projectname, teamname=teamname)
        result = {'result': 1, 'message': r"获取项目成功！", "project": project.to_dic()}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def get_project_list(request):  # 获取当前团队的项目列表
    try:
        json_str = request.body
        json_obj = json.loads(json_str)
    except json.JSONDecodeError as e:
        result = {'code': 10112, 'error': 'Invalid JSON data'}
        return JsonResponse(result)
    try:
        teamname = json_obj['teamname']
        team = Team.objects.get(teamname=teamname)
    except Exception as e:
        result = {'result': 0, 'message': r"请先登录!"}
        return JsonResponse(result)
    result = {'result': 1, 'message': r"获取项目列表成功！", "team": team.to_dic(),
              "project_list": get_project_list_detail(team.teamid)}
    return JsonResponse(result)


def delete_project(request, username):  # 删除项目
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        teamname = json_obj['teamname']
        projectname = json_obj['projectname']
        user = get_object_or_404(User, username=username)
        team = get_object_or_404(Team, teamname=teamname)
        member = get_object_or_404(TeamMember, userid=user, teamid=team)
        project = get_object_or_404(Project, projectname=projectname, teamid=team)
        team_to_project = get_object_or_404(TeamToProject, projectid=project.projectid, teamid=team.teamid)

        if member.role > 0 or project.creatorid == member.userid:
            # 删除项目及关联的TeamToProject对象
            project.delete()
            team_to_project.delete()
            result = {'result': 1, 'message': r"项目删除成功！"}
            return JsonResponse(result)
        else:
            return JsonResponse({'code': 10010, 'error': '用户权限不够'})

    result = {'result': 0, 'message': r"请求类型错误！"}
    return JsonResponse(result)


def rename_project(request):  # 重命名项目
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        projectname = json_obj['projectname']
        teamname = json_obj['teamname']
        newprojectname = json_obj['newprojectname']
        team = get_object_or_404(Team, teamname=teamname)
        # 获取要重命名的项目
        project = get_object_or_404(Project, projectname=projectname, teamid=team.teamid)

        # 更新项目名称
        project.projectname = newprojectname
        project.save()

        result = {'result': 1, 'message': r"项目重命名成功！", 'projectname': project.projectname}
        return JsonResponse(result)

    result = {'result': 0, 'message': r"请求类型错误！"}
    return JsonResponse(result)


def copy_project(request, username):  # 复制项目
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        projectname = json_obj['projectname']
        teamname = json_obj['teamname']
        newprojectname = json_obj['newprojectname']

        team = get_object_or_404(Team, teamname=teamname)
        user = get_object_or_404(User, username=username)
        oldproject = get_object_or_404(Project, projectname=projectname)

        copy_projectname = newprojectname

        project = Project.objects.create(projectname=copy_projectname, teamid=team, creatorid=user)
        TeamToProject.objects.create(teamid=team.teamid, projectid=project.projectid)

        if Document.objects.filter(projectid=oldproject).exists():
            olddocuments = Document.objects.filter(projectid=oldproject)
            for olddocument in olddocuments:
                Document.objects.create(documenttitle=olddocument.documenttitle,
                                        documentcontent=olddocument.documentcontent, projectid=project)

        if PrototypePage.objects.filter(projectid=oldproject).exists():
            oldpages = PrototypePage.objects.filter(projectid=oldproject)
            for oldpage in oldpages:
                PrototypePage.objects.create(pagename=oldpage.pagename, pagesize=oldpage.pagesize,
                                             pagecontent=oldpage.pagecontent, projectid=project)

        result = {'result': 1, 'message': r"项目创建副本成功！", 'projectname': project.projectname}
        return JsonResponse(result)

    result = {'result': 0, 'message': r"请求类型错误！"}
    return JsonResponse(result)


def search_project(request, username):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        #type = json_obj['type']
        query = json_obj['query']
        team_name = json_obj['team_name']
        #if type == 'project':
        team = get_object_or_404(Team, teamname=team_name)
        projects = Project.objects.filter(Q(projectname__icontains=query), teamid=team)
        project_list = []
        for project in projects:
            a_project = project.to_dic()
            project_list.append(a_project)
        result = {'result': 1, 'message': r"查询成功！", "project": project_list}
    else:
        result = {'result': 0, 'message': r"请求方式错误！"}
    return JsonResponse(result)
