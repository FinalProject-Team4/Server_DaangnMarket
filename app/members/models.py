from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.CharField(max_length=30, unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    phone = models.CharField(max_length=11)
    # buyer_review =
    # seller_review =
