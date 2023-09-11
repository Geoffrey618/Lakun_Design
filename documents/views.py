import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from tools.user_dec import *
import base64
import hashlib
import time
import random

from django.core.cache import cache
from django.urls import reverse
from django.contrib.auth import authenticate, user_logged_in, user_logged_out
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from django.conf import settings

from user.models import *
from django.conf import settings

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

channel_layer = get_channel_layer()


def create_document(request):  # 创建文档
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        project_id = json_obj['project_id']
        documenttitle = json_obj['document_title']
        documentcontent = json_obj['document_content']
        foldername = json_obj['foldername']
        project = Project.objects.get(projectid=project_id)
        try:
            existing_document = Document.objects.get(projectid=project, documenttitle=documenttitle)
            # 如果找到现有记录，删除它
            existing_document.delete()
        except ObjectDoesNotExist:
            pass  # 如果记录不存在，则无需删除

        document = Document(projectid=project, documenttitle=documenttitle, documentcontent=documentcontent)
        document.save()

        folder = Folder(foldertitle=foldername, documentid=document, projectid=project)
        folder.save()
        return JsonResponse({'success': True, 'documentid': document.documentid})
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def create_folder(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        project_id = json_obj['project_id']
        foldername = json_obj['foldername']

        project = Project.objects.get(projectid=project_id)

        document = Document(projectid=project, documenttitle='init', documentcontent='init')
        document.save()

        folder = Folder(foldertitle=foldername, documentid=document, projectid=project)
        folder.save()
        return JsonResponse({'success': True, 'folderid': folder.folderid})
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def get_dic(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        project_id = json_obj['project_id']
        project = Project.objects.get(projectid=project_id)
        projectfolders = Folder.objects.filter(projectid=project)
        rowfolders = [folder.foldertitle for folder in projectfolders]
        folders = []
        dic_list = []
        for folder2 in rowfolders:
            if folder2 not in folders:
                folders.append(folder2)

        for folder3 in folders:
            dic = {'foldername': folder3, 'label': folder3}
            childrenlist = []
            documents = Folder.objects.filter(foldertitle=folder3, projectid=project)
            for document in documents:
                if document.documentid.documenttitle != document.foldertitle:
                    dic1 = {'foldername': document.foldertitle, 'label': document.foldertitle}
                    dic1['children'] = []
                    childrenlist.append(dic1)
            dic['children'] = childrenlist
            dic_list.append(dic)

        result = {'result': dic_list}
        return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def edit_document(request, documentid):  # 编辑文档内容
    document = get_object_or_404(Document, documentid=documentid)

    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        document_title = json_obj['document_title']
        document_content = json_obj['document_content']

        document.documenttitle = document_title
        document.documentcontent = document_content
        document.save()

        return redirect('document_detail', documentid=document.documentid)
    else:
        return render(request, 'documents/edit_document.html', {'document': document})


def document_detail(request):  # 查看文档内容

    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        documentid = json_obj['documentid']
        document = get_object_or_404(Document, documentid=documentid)
        document_data = {
            'documentid': document.documentid,
            'projectid': document.projectid.projectid,
            'documenttitle': document.documenttitle,
            'documentcontent': document.documentcontent,
            'versions': []
        }
        return JsonResponse(document_data)
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def save_document(request, documentid):  # 保存文档内容
    document = get_object_or_404(Document, documentid=documentid)
    json_str = request.body
    json_obj = json.loads(json_str)
    content = json_obj['content', '']

    version = DocumentVersion(
        documentid=document,
        versioncontent=content,
        timestamp=datetime.now()
    )
    version.save()

    document.documentcontent = content
    document.save()

    # 发送 WebSocket 消息通知其他用户文档内容已更新
    async_to_sync(channel_layer.group_send)(
        f'document_{documentid}',
        {
            'type': 'document_update',
            'documentid': documentid,
            'content': content,
        }
    )

    return JsonResponse({'message': 'Document saved successfully.'})


def receive_message(request):
    if request.method == 'POST':
        try:
            json_str = request.body
            json_obj = json.loads(json_str)
            stringname = json_obj['documentcontent']
            sendername = json_obj['username']
            documenttitle = json_obj['documenttitle']
            usernames = []
            parts = stringname.split(",")
            send_user = User.objects.get(username=sendername)
            turnteam = UserToTeam.objects.get(userid=send_user.userid)
            testteam = Team.objects.get(teamid=turnteam.teamid)
            for part in parts:
                usernames.append(part)

            if usernames:
                for receivername in usernames:
                    user = User.objects.get(username=receivername)
                    chat_message = ChatMessage(content='您在文档' + documenttitle + '中收到了一条@消息',
                                               status='unread',
                                               mentioneduserid=user, senderid=send_user, teamid=testteam)
                    chat_message.save()

            return JsonResponse({'message': 'Chat message created successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)
