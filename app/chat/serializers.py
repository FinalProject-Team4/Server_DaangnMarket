from rest_framework import serializers

from chat.models import Room, Message


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            'name', 'id', 'members'
        )


class RoomCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = (
            'name', 'id'
        )


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('room', 'content', 'created', 'sender', 'receiver')


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'content',
        )
