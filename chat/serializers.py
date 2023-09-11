from user.models import *
from rest_framework import serializers
from django.shortcuts import get_object_or_404


class ChatMessageSerializer(serializers.Serializer):
    attachments = serializers.ListField(child=serializers.CharField(), allow_empty=True)
    created = serializers.DateTimeField()
    custom_json = serializers.DictField()
    id = serializers.IntegerField()
    sender = serializers.DictField()
    sender_username = serializers.CharField(source='sender.username', max_length=255)  # 修改此行

    text = serializers.CharField()

    def create(self, validated_data):
        sender_username = validated_data.pop('sender_username')  # 提取 sender_username
        sender = get_object_or_404(User, username=sender_username)

        return ChatMessage.objects.create(content=validated_data['text'], timestamp=validated_data['created'], senderid=sender)