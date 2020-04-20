from push_notifications.api.rest_framework import GCMDeviceSerializer
from rest_framework import serializers

from notification.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    sender = serializers.CharField(source='sender.name')
    receiver = serializers.CharField(source='receiver.name')

    class Meta:
        model = Notification
        depth = 0
        fields = (
            'sender', 'receiver', 'title', 'body',
        )
