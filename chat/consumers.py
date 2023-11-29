

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.models import Chat,ChatMember,Message
from chat.serializers import MessageSerializer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from main.functions import send_common_mail

import django
django.setup()

from account.models import Account

 
 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self,):
        user = self.scope["user"]
        self.roomGroupName = "user" + str(user.id)
        print(self.roomGroupName)
        await self.channel_layer.group_add(
            self.roomGroupName ,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self , close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName ,
            self.channel_layer
        )
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)

        data["sender_id"] = self.scope["user"].id

        msg_data ={
            'chat_id': data["chat"],
            'sender_id': self.scope["user"].id,
            'content':data["content"],
            'msg_type':data["msg_type"]
        }
        msg_data = await sync_to_async(get_last_id)(msg_data)



        members = msg_data["chat_members"]
        print(members)
        data["id"] = msg_data["id"]

        for member in members:
            
            await self.channel_layer.group_send(
                "user" + str(member),{
                    "type" : "sendMessage" ,
                    "data" : {**data}
                })


    async def sendMessage(self , event) :
        await self.send(text_data = json.dumps(event["data"]))


def get_last_id(msg_data):
    last_msg = Message.objects.create(**msg_data)
    msg_data["id"] = last_msg.id
    admins = list(Account.objects.filter(is_admin=True).values_list("id",flat=True))
    chat_members = list(ChatMember.objects.filter(chat__id = msg_data["chat_id"]).values_list("account__id",flat=True))
    msg_data["chat_members"]= list(set(admins) | set(chat_members))

    chat = Chat.objects.get(pk = msg_data["chat_id"])
    if(Account.objects.filter(pk=msg_data["sender_id"],is_admin=False).exists()):
        chat.unread+=1
        chat.save()
    else:
        chat.unread=0
        chat.save()

        s = set(admins)
        for x in chat_members:
            if x not in s:
                account = Account.objects.filter(pk=x).first()
                to_email = account.email
                subject = "New message recieved from careerpro check with your Mobile App"
                html_context = {
                    "title":"New message recieved from careerpro check with your Mobile App",
                    "data":[
                        {
                            "label":">>:",
                            "value":msg_data["content"]
                        }
                    ]
                }
                send_common_mail(html_context,to_email,subject)



    return(msg_data)

def create_msg(msg):
    last_msg = Message.objects.all().first()
    return(last_msg.id +1)