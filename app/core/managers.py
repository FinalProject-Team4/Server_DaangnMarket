import random
import string

from django.db import models
from django.contrib.auth.models import UserManager
from django.utils import timezone


def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


class CustomModelManager(UserManager, models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.created = timezone.now()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('user must have a username')
        uid = random_string(28)
        user = self.model(
            username=username,
            uid=uid,
            email=email,
            password=password,
            **extra_fields
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self.db)
        return user
