from django.shortcuts import render
from push_notifications.api.rest_framework import GCMDeviceSerializer
from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.authentication import TokenAuthentication

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from members.models import User


# device 등록
from notification.serializers import NotificationSerializer


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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


# FCM 발송
class ApiSendFcm(CreateAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        sender = GCMDevice.objects.get(user=user)
        receiver = GCMDevice.objects.get(user=user)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            notification = serializer.save(sender=sender, receiver=receiver)
            receiver.send_message(notification.body, extra={"title": notification.title})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




