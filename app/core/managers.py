from django.db import models
from django.contrib.auth.models import UserManager
from django.utils import timezone


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
