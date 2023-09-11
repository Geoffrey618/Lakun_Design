from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone

from user.models import *


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_name = self.scope['url_route']['kwargs']['room_name']
        username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'chat_room_' + room_name

        # 加入房间群组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开房间群组
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        username = self.scope['url_route']['kwargs']['username']
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = self.scope['user']
        chat_message = ChatMessage.objects.create(
            teamid=self.room_name,  # Assuming teamid is the same as room_name
            senderid=sender,
            content=message,
            timestamp=timezone.now()
        )
        # 发送消息到房间群组
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'message_id': chat_message.messageid,
            }
        )
        # 处理 @ 提及逻辑
        if message.startswith('@all'):

            if TeamMember.objects.get(userid=(User.objects.get(username=username)).id).role == 1 or TeamMember.objects.get(userid=(User.objects.get(username=username)).id).role == 2:
                # 发送消息给整个团队的聊天室组
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message': message,
                        'sender': sender.username,
                    }
                )
                await self.channel_layer.group_send(
                    'notification_channel_all',
                    {
                        'type': 'notification.message',
                        'message': f'@所有人：{message}',
                    }
                )
            else:
                # Notify user about restricted mention
                await self.send_notification("You don't have permission to mention in this way.")

        elif message.startswith('@'):
            mentioned_usernames = message[1:].split()
            # 处理单独提及的逻辑，发送通知给被提及的用户
            for mentioned_username in mentioned_usernames:
                chat_message.mentioneduserid = User.objects.get(username=mentioned_username).userid
                await self.channel_layer.send(
                    'notification_channel_' + mentioned_username,
                    {
                        'type': 'notification.message',
                        'message': f'你被提及了：{message}',
                    }
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat.message',
                        'message': message,
                        'sender': sender.username,
                    }
                )
        else:
            # 普通消息，发送给整个团队的聊天室组
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender': sender.username,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        message_id = event['message_id']
        # 发送消息到 WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender,
            'message_id': message_id
        }))

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
        }))

    async def send_notification(self, message):
        await self.channel_layer.send(
            'notification_channel_' + self.scope['user'].username,
            {
                'type': 'notification.message',
                'message': f'你有一条新消息：{message}',
            }
        )

    async def mark_message_as_read(self, message_id):
        try:
            message = ChatMessage.objects.get(messageid=message_id)
            message.mark_as_read()
        except ChatMessage.DoesNotExist:
            pass
        await self.notification_message("消息已标记为已读")


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'notification_channel_' + username

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def notification_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
        }))

    async def send_notification(self, message):
        await self.channel_layer.send(
            'notification_channel_' + self.scope['user'].username,
            {
                'type': 'notification.message',
                'message': f'你有一条新消息：{message}',
            }
        )

    async def mark_message_as_read(self, message_id):
        try:
            message = ChatMessage.objects.get(messageid=message_id)
            message.mark_as_read()
        except ChatMessage.DoesNotExist:
            pass
        await self.notification_message("消息已标记为已读")

    async def get_message_list(self):
        user = self.scope['url_route']['kwargs']['username']
        messages = ChatMessage.objects.filter(senderid=user)
        message_list = []
        for message in messages:
            message_list.append({
                'message_id': message.messageid,
                'content': message.content,
                'timestamp': message.timestamp,
                'status': message.status,
            })
        await self.send(text_data=json.dumps({
            'type': 'message_list',
            'messages': message_list,
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'delete_message':
            message_id = data.get('message_id')
            await self.delete_message(message_id)
        elif action == 'get_message_list':
            await self.get_message_list()

    async def delete_message(self, message_id):
        try:
            message = ChatMessage.objects.get(messageid=message_id)
            message.delete()
            await self.send_notification("消息已删除")
        except ChatMessage.DoesNotExist:
            await self.send_notification("消息不存在")

    async def mark_all_as_read(self):
        user = self.scope['user']
        unread_messages = ChatMessage.objects.filter(senderid=user, status='unread')
        for message in unread_messages:
            await self.mark_message_as_read(message.messageid)
        await self.send_notification("所有消息已标记为已读")

    async def delete_all_messages(self):
        user = self.scope['user']
        user_messages = ChatMessage.objects.filter(senderid=user)
        for message in user_messages:
            await self.delete_message(message.messageid)
        await self.send_notification("所有消息已删除")




    # class MessageConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         pass
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#
#         await self.process_message_logic(message)
#
#         await self.send(text_data=json.dumps({
#             'message': message,
#         }))
#
#     async def process_message_logic(self, message):
#         await self.save_message_to_database(message)
#         await self.mark_message_as_read(message)
#         await self.send_notification(message)
#
#     async def save_message_to_database(self, message):
#             # Replace this with actual logic to save the message to the database
#         pass
#
#     async def mark_message_as_read(self, message):
#             # Replace this with actual logic to mark the message as read
#         pass
#
#     async def send_notification(self, message):
#         await self.channel_layer.send(
#             'notification_channel_' + self.scope['user'].username,
#             {
#                 'type': 'notification.message',
#                 'message': f'你有一条新消息：{message}',
#             }
#         )
