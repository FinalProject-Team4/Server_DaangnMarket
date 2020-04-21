from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import *
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


# exceptions
# 1. auth 없을때
# 2. 파베에러(이상한 토큰, expired)
class UserBackend(object):
    def authenticate(self, request, auth=None):
        data = {
            'uid': auth.get('uid'),
            'phone': auth.get('phone_number'),
            'username': auth.get('username', None),
            'avatar': auth.get('avatar', None)
        }
        try:
            user = User.objects.get(uid=data['uid'])
        except User.DoesNotExist:
            if data['username']:
                data.update({
                    'is_staff': False,
                    'is_superuser': False,
                    'created': timezone.now(),
                })
                user = User.objects.create(**data)
                if data['avatar']:
                    user.avatar = data['avatar']
                    user.save()
                return user
            raise AuthenticationFailed
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
