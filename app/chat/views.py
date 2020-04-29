from django.shortcuts import render
from push_notifications import apns
from push_notifications.exceptions import NotificationError
from push_notifications.models import GCMDevice
from rest_framework import status

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from chat.models import Room, Message
from chat.serializers import RoomSerializer, MessageSerializer, RoomCreateSerializer, MessageCreateSerializer

# get 방정보(get_or_create room)
# post 메세지 보내기 + 노티
#### USER 정보 get
### USER가 판매 중인 상품


# 만들어진 Room DB에 저장
from members.models import User


class ApiRoomSave(CreateAPIView):
    serializer_class = RoomCreateSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        receiver_username = request.data['receiver']
        receiver = User.objects.get(username=receiver_username)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(members=[user, receiver])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomList(ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        user = self.request.user
        list = Room.objects.filter(members__in=[user])
        return list


class ApiMessageSave(CreateAPIView):
    serializer_class = MessageCreateSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        receiver_username = request.data['receiver']
        room_id = request.data['room']
        room = Room.objects.get(id=room_id)
        receiver = User.objects.get(username=receiver_username)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=sender, receiver=receiver, room=room)
            device = GCMDevice.objects.get(name=receiver.username)
            try:
                device.send_message('채팅을 확인해주세요.', extra={"title": '채팅 알람이 들어왔습니다.', "type": "chat"}, badge=1)

            except NotificationError(Exception):
                print(Exception)
            except apns.APNSError(NotificationError):
                print(NotificationError)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiMessageList(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room')
        room = Room.objects.get(id=room_id)
        list = Message.objects.filter(room=room)
        return list
