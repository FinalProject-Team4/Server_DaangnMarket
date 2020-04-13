from django.db import models
from push_notifications.models import GCMDevice


class Notification(models.Model):
    sender = models.ForeignKey(GCMDevice, on_delete=models.CASCADE, null=True, blank=True, related_name='noti_sender')
    receiver = models.ForeignKey(GCMDevice, on_delete=models.CASCADE, related_name='noti_receiver')

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.CharField(max_length=200)
    is_succeed = models.BooleanField(default=False)

    def __str__(self):
        if self.sender is None:
            return f'{self.title} -> {self.receiver.name}'
        else:
            return f'{self.sender.name} -> {self.title} -> {self.receiver.name}'

    def to_message(self):
        message = {
            "title": self.title,
            "body": self.body,
        }
        return message




