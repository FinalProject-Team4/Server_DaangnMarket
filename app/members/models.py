from django.contrib.auth.models import AbstractUser
from django.db import models

from core import models as core_models


def content_file_name(instance, filename):
    return '/'.join(['avatar', f'{instance.username}-{filename}'])


class User(core_models.TimeStampedModel, AbstractUser):
    uid = models.CharField(max_length=28, unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to=content_file_name, blank=True)
    phone = models.CharField(max_length=13)
    # buyer_review =
    # seller_review =app
