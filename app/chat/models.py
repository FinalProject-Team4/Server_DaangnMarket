from django.db import models
from django.contrib.auth import get_user_model

from core.models import TimeStampedModel as CoreModel

User = get_user_model()


class Room(CoreModel):
    name = models.CharField(max_length=30)
    member = models.ManyToManyField(User, related_name="rooms", on_delete=models.CASCADE)

    @property
    def messages(self):
        return self.room_messages


class Message(CoreModel):
    content = models.TextField
    room = models.ForeignKey(Room, related_name="room_messages", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
