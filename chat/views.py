from django.shortcuts import render
import json
import random
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from django.shortcuts import get_object_or_404
from .serializers import *

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
from django.http import JsonResponse, HttpResponse
import json
import jwt
from django.conf import settings

# from tools.user_dec import check_token
from user.models import *
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def deal_string(input_string):

    usernames = []

    # 使用 "@" 分割输入字符串
    parts = input_string.split("@")

    # 遍历分割后的部分，从第二个部分开始（索引1）
    for part in parts[1:]:
        # 去除空格并添加到域名列表中
        username = part.strip().split()[0]
        usernames.append(username)

    return usernames


def my_websocket_view(request, chat_id):
    if request.method == 'WEBSOCKET':
        # 处理 WebSocket 连接
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)('chat_id' + chat_id, {'type': 'websocket.connect'})
        return HttpResponse("WebSocket connection established.")


def create_public_chat(request, team_id):
    team = Team.objects.get(teamid=team_id)
    # 创建公开群聊
    public_chat = PublicChat.objects.create(team=team)
    # 将所有团队成员添加为群聊的成员
    team_members = TeamMember.objects.filter(teamid=team)
    for member in team_members:
        PublicChatMember.objects.create(chatid=public_chat, userid=member.userid)
    return JsonResponse({"code": 200, "message": "Public chat 创造成功."})


def send_chat_message(request, chat_id):
    data = request.POST
    content = data.get('content')
    sender = User.objects.get(username=data.get('sender'))
    chat = PublicChat.objects.get(chatid=chat_id)
    message = ChatMessage.objects.create(chatid=chat, senderid=sender, content=content)
    return JsonResponse({"code": 200, "message": "Message 发送成功."})


def mention_user(request, message_id):
    data = request.POST
    message = ChatMessage.objects.get(messageid=message_id)
    mentioned_usernames = data.getlist('mentioned_users')
    mentioned_users = User.objects.filter(username__in=mentioned_usernames)
    message.mentioned_users.set(mentioned_users)
    message.save()
    return JsonResponse({"code": 200, "message": "Users mentioned 成功."})


def get_message_list(request, username):
    user = get_object_or_404(User, username=username)
    received_messages = ChatMessage.objects.filter(mentioneduserid=user)
    unread_messages = received_messages.filter(status='unread')
    read_messages = received_messages.filter(status='read')

    unread_messages_data = [
        {
            'id': message.messageid,
            'sender': message.senderid.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for message in unread_messages
    ]

    read_messages_data = [
        {
            'id': message.messageid,
            'sender': message.senderid.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for message in read_messages
    ]

    return JsonResponse({
        'unread_messages': unread_messages_data,
        'read_messages': read_messages_data,
    })


def mark_message_as_read(request, messageid):
    message = get_object_or_404(ChatMessage, messageid=messageid)
    message.mark_as_read()
    return JsonResponse({'message': 'Message marked as read'})


def message_detail(request, messageid):
    message = get_object_or_404(ChatMessage, messageid=messageid)
    # 标记消息为已读
    if message.status == 'unread':
        message.mark_as_read()

    # 这里可以根据消息产生位置生成相应的跳转链接
    # 例如：location_link = generate_location_link(message.location)
    location_link = "https://example.com/location/link"

    message_data = {
        'id': message.messageid,
        'sender': message.senderid.username,
        'content': message.content,
        'timestamp': message.timestamp,
        'location_link': location_link,
    }
    return JsonResponse(message_data)


def delete_message(request, messageid):
    message = get_object_or_404(ChatMessage, messageid=messageid)
    message.delete()
    return JsonResponse({'message': 'Message deleted'})


def mark_all_unread_as_read(request, username):
    user = get_object_or_404(User, username=username)
    unread_messages = ChatMessage.objects.filter(senderid=user, status='unread')
    for message in unread_messages:
        message.mark_as_read()
    return JsonResponse({'message': 'All unread messages marked as read'})


def delete_all_messages_for_user(request, username):
    user = get_object_or_404(User, username=username)
    user_messages = ChatMessage.objects.filter(senderid=user)
    user_messages.delete()
    return JsonResponse({'message': 'All messages for the user have been deleted'})


def receive_chat_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_data = data.get('message', {})
            sender_data = message_data.get('sender', {})
            text = message_data.get('text')
            created = message_data.get('created')
            chat_dic = data.get('chat')
            people_list = chat_dic['people']

            sendername = sender_data.get('username')
            isall = 0
            atnames = deal_string(text)
            for name in atnames:
                if name == "all":
                    usernames = [person.get('person').get('username') for person in people_list]
                    isall = 1

            if isall == 0:
                usernames = []
                for name in atnames:
                    usernames.append(name)
            print(isall)
            send_user = User.objects.get(username=sendername)
            turnteam = UserToTeam.objects.get(userid=send_user.userid)
            testteam = Team.objects.get(teamid=turnteam.teamid)

            if usernames:
                for receivername in usernames:
                    if receivername != sendername:
                        user = User.objects.get(username=receivername)
                        chat_message = ChatMessage(content=text, status='unread', timestamp=created, mentioneduserid=user,
                                                   senderid=send_user, teamid=testteam)
                        chat_message.save()

            return JsonResponse({'message': 'Chat message created successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)


def prompt_chat(request):
    return JsonResponse({'message': 'You have a new conversation in the chat room'})
