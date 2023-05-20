from urllib import response
from django.shortcuts import get_object_or_404, render
# from main.permissions import IsUser
from chat.serializers import ChatSerializer,ChatMemberSerializer,MessageSerializer,MessageFileSerializer
from .models import *
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from  rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from main.functions import get_auto_id





from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})



class ChatViewSet(ModelViewSet):
    serializer_class = ChatSerializer
    # queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    # search_fields = ['student__user__username','student__user__first_name','student__user__last_name']
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        chat_member = ChatMember.objects.filter(account=user).prefetch_related('chat')

        return chat_member.chat.objects.filter()
   
    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     queryset = queryset.get(pk=pk)
    #     queryset.unread = 0
    #     print("retrive ///")
    #     queryset.save()
    #     serializer = ChatSerializer(queryset, context={'request': self.request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        if(request.user.is_admin):
            queryset = Chat.objects.all().order_by("-unread")
        else:
            members = ChatMember.objects.filter(account=request.user).values_list("chat__pk")
            queryset = Chat.objects.filter(pk__in = members)
            if(not queryset):
                queryset = Chat.objects.create(
                    name = request.user.full_name,
                    email = request.user.email
                )
                ChatMember.objects.create(
                    chat = queryset,
                    account = request.user
                )
                admins = Account.objects.filter(is_admin=True)
                for admin in admins:
                    ChatMember.objects.create(
                    chat = queryset,
                    account = admin
                )
                queryset = Chat.objects.filter(pk = queryset.pk)
                
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)




class ChatMemberViewSet(ModelViewSet):
    serializer_class = ChatMemberSerializer
    queryset = ChatMember.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    # search_fields = ['student__user__username','student__user__first_name','student__user__last_name']
    
    def list(self, request):
        queryset = ChatMember.objects.all()
        serializer = ChatMemberSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        serializer = ChatMemberSerializer(data=request.data ,context={'request': self.request})
        if(serializer.is_valid() and (not ChatMember.objects.filter(account=request.user).exists())):
            serializer.save(account = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"error":"Already exists !"}
            return Response(data,status=status.HTTP_403_FORBIDDEN)




class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    # search_fields = ['student__user__username','student__user__first_name','student__user__last_name']

    def list(self, request):
        chat = self.request.query_params.get('chat')
        if(chat):
            queryset = Message.objects.filter(chat=chat)
            if(request.user.is_admin):
                Chat.objects.filter(pk=chat).update(unread=0)
        else:
            queryset = []

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class MessageFileViewSet(ModelViewSet):
    serializer_class = MessageFileSerializer
    queryset = MessageFile.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]

    # def retrieve(self, request, pk=None):
    #     item = get_object_or_404(self.queryset, pk=pk)
    #     serializer = MessageFileSerializer(item)
    #     serializer = MessageFileSerializer(item, context={"request": request})
    #     serializer = {}
    #     return Response({},status=status.HTTP_200_OK)
    # def get_serializer(self):
    #     print("get_serializer ../")
    #     return MessageFileSerializer(context={"request": self.request})

    def create(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        if(serializer.is_valid()):
            self.perform_create(serializer)
            data = serializer.data
            data["msg_file"] = data["msg_file"].replace("http://", "https://")
            request.build_absolute_uri(data["msg_file"])
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {"error":serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

