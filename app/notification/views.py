from django.shortcuts import render
from push_notifications.api.rest_framework import GCMDeviceSerializer
from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from members.models import User


# device 등록
from notification.models import Notification
from notification.serializers import NotificationSerializer, NotificationNoticeSerializer


class ApiFcmDeviceRegister(CreateAPIView):
    serializer_class = GCMDeviceSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        print('ApiFcmDeviceRegister')
        user = self.request.user
        registration_id = request.data.get('registration_id')
        data = {'name': user.username,
                'registration_id': registration_id,
                'cloud_message_type': 'FCM', }
        print('data : ', data)
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


# FCM 발송
class ApiSendFcm(CreateAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = self.request.user

        sender = GCMDevice.objects.get(name=user.username)
        receiver = GCMDevice.objects.get(name=user.username)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            notification = serializer.save(sender=sender, receiver=receiver)
            receiver.send_message(notification.body, extra={"title": notification.title})
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 알림 발송
class ApiSendNotice(CreateAPIView):
    serializer_class = NotificationNoticeSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return Response('this user is not admin', status=status.HTTP_401_UNAUTHORIZED)
        sender = GCMDevice.objects.get(name='관리자')

        receivers = GCMDevice.objects.all().exclude(name='관리자')
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            for receiver in receivers:
                notification = serializer.save(sender=sender, receiver=receiver)
                if notification.title == '':
                    receiver.send_message(notification.body)
                else:
                    receiver.send_message(notification.body,
                                          extra={"title": notification.title, "type": "notice"},
                                          badge=1)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 채팅 알림 발송
class ApiSendChat(CreateAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        receiver_username = request.data.get('receiver')
        sender = GCMDevice.objects.get(name=user.username)
        receiver = GCMDevice.objects.get(name=receiver_username)
        notification = Notification.objects.create(sender=sender,
                                                   receiver=receiver,
                                                   title='채팅 알람이 들어왔습니다.',
                                                   body='채팅을 확인해주세요.')
        receiver.send_message(notification.body,
                              extra={"title": notification.title, "type": "chat"},
                              badge=1)
        return Response(status=status.HTTP_200_OK)


# 알림 리스트 가져오기
class ApiListNotice(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        receiver = GCMDevice.objects.get(name=user.username)
        notifications = Notification.objects.filter(receiver=receiver)
        return notifications


# 알림 삭제
class ApiDeleteNotice(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        pass

