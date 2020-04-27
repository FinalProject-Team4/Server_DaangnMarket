from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from core.models import TimeStampedModel as CoreModel
from location.models import Locate


def content_file_name(instance, filename):
    return '/'.join(['avatars', f'{instance.username}-{filename}'])


class User(CoreModel, AbstractUser):
    uid = models.CharField(
        max_length=28, unique=True, primary_key=True, help_text='파이어베이스 uid')
    username = models.CharField(
        max_length=30, unique=True, help_text='닉네임')
    avatar = models.ImageField(
        upload_to=content_file_name, blank=True, default='media/avatars/carrot-default.png', help_text='프로필 사진')
    phone = models.CharField(
        max_length=13, help_text='핸드폰 번호')
    selected_locations = models.ManyToManyField(
        Locate, through='SelectedLocation', related_name='users_select', help_text='내 동네 선택')

    # buyer_review =
    # seller_review =app
    @property
    def messages(self):
        return self.user_messages

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저'


class SelectedLocation(CoreModel):
    locate = models.ForeignKey(
        Locate, related_name='user_selected_locations', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='user_selected_locations', on_delete=models.CASCADE)
    verified = models.BooleanField(
        default=False, help_text='동네 인증 여부')
    activated = models.BooleanField(
        default=False, help_text='선택된 동네')
    distance = models.IntegerField(
        default=1000, help_text='동네 포함 범위')

    def clean(self):
        cnt = self.user.user_selected_locations.count()
        if cnt > 2:
            raise ValidationError(f'{self.user.username}님은 이미 2개 선택 했습니다')

    class Meta:
        verbose_name = '내 동네'
        verbose_name_plural = '내 동네'