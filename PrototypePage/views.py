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
from PIL import Image
from io import BytesIO
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


def create_page(request):
    if request.method == 'POST':
        try:
            json_obj = json.loads(request.body.decode('utf-8'))
            projectid = json_obj['projectid']
            project = Project.objects.get(projectid=projectid)
            pagecontent = json_obj['canvasData']
            pagesize = json_obj['pagesize']

            pagename = json_obj['pagename']
            try:
                existing_page = PrototypePage.objects.get(projectid=projectid, pagename=pagename)

                # 如果找到现有记录，删除它
                existing_page.delete()
            except ObjectDoesNotExist:
                pass  # 如果记录不存在，则无需删除

            page = PrototypePage(pagecontent=pagecontent,projectid=project,pagename=pagename,pagesize=pagesize)
            page.save()

            return JsonResponse({'success': True, 'page_id': page.pageid})

        except json.JSONDecodeError:
            result = {'result': 0, 'message': 'JSON 解析错误'}
            return JsonResponse(result)
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def edit_page(request, page_id):
    page = get_object_or_404(PrototypePage, pageid=page_id)

    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        page_content = json_obj['page_content']

        page.pagecontent = page_content
        page.save()

        return JsonResponse({'success': True, 'page_id': page.pageid})
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def export_page(request, page_id):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        canvas_data = json_obj['canvas_data']

        # 将Canvas数据转换为图像
        image = Image.open(BytesIO(base64.b64decode(canvas_data)))

        # 保存图像到数据库或其他位置
        # 请根据实际需求进行修改
        page = get_object_or_404(PrototypePage, pageid=page_id)
        page.image = image
        page.save()

        return JsonResponse({'success': True})
    else:
        result = {'result': 0, 'message': r"请求类型错误！"}
        return JsonResponse(result)


def get_page_content(request):
    if request.method == 'POST':
        json_str = request.body
        json_obj = json.loads(json_str)
        pagename = json_obj['pagename']
        projectid = json_obj['projectid']

        # 在PrototypePage中查找匹配的页面
        page = get_object_or_404(PrototypePage, pagename=pagename, projectid=projectid)

        # 将页面内容(pagecontent)中的单引号替换为双引号
        pagecontent_json = page.pagecontent.replace("'", "\"")

        # 将页面内容(pagecontent)传回前端
        return JsonResponse({'success': True, 'pagecontent': pagecontent_json})
    else:
        result = {'result': 0, 'message': '请求类型错误！'}
        return JsonResponse(result)