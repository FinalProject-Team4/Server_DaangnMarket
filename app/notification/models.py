from django.db import models
from push_notifications.models import GCMDevice


class Notification(models.Model):
    sender = models.ForeignKey(
        GCMDevice, on_delete=models.CASCADE, null=True, blank=True, related_name='noti_sender')
    receiver = models.ForeignKey(
        GCMDevice, on_delete=models.CASCADE, related_name='noti_receiver')

    title = models.CharField(
        max_length=200, help_text='알림 제목', null=True, blank=True)
    subtitle = models.CharField(
        max_length=200, blank=True, help_text='알림 부제목')
    body = models.CharField(
        max_length=200, help_text='알림 내용')
    type = models.CharField(
        default='notice', max_length=10
    )
    created = models.DateTimeField(auto_now_add=True)
    is_succeed = models.BooleanField(
        default=False, help_text='알림 성공 여부')

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
