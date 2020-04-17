from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import TimeStampedModel as CoreModel


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

    # buyer_review =
    # seller_review =app

    class Meta:
        verbose_name = '유저'
        verbose_name_plural = '유저'
