from rest_framework import serializers
# from careerpro import student
from account.models import Account
from account.serializers import AccountSerializer, RegistrationSerializer
from main.functions import get_auto_id, password_generater, send_common_mail
from student.models import Specialization, Student,JobApplication
from chat.models import Chat,ChatMember,Message,MessageFile
from django.db import transaction

class ChatSerializer(serializers.ModelSerializer):
    member = serializers.StringRelatedField(many=True)
    class Meta:
        model = Chat
        fields = [
            'id',
            'name',
            'email',
            'unread',
            'is_group',
            'member'
        ]

class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = [
            'id',
            'chat',
            'account'
        ]
        extra_kwargs = {
            'account':{'read_only': True},
            'id':{'read_only': True},
        }

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.email',read_only = True)
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'sender',
            'content',
            'timestamp',
            'read',
            'sender_name',
            'msg_type'
        ]

class MessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageFile
        fields = [
            'id',
            'msg_file',
        ]
        extra_kwargs = {
            'account': {'read_only': True},
        }

    def create(self,validated_data):
        messageFile = MessageFile.objects.create(
            **validated_data,
            account = self.context['request'].user
        )
        # messageFile.msg_file = "self.request.build_absolute_uri(messageFile.msg_file)"
        return messageFile
