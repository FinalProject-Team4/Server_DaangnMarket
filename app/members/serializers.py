from django.contrib.auth import get_user_model
from config.settings.base import fb_auth
from rest_framework import serializers, status
from rest_framework.response import Response

from location.serializers import LocateSerializer
from members.models import SelectedLocation
from location.models import Locate

User = get_user_model()


# 유저 모델
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(allow_empty_file=True)
    Authorization = serializers.SerializerMethodField(method_name='get_authorization')

    class Meta:
        model = User
        fields = [
            'uid',
            'avatar',
            'phone',
            'created',
            'updated',
            'username',
            'Authorization',
        ]
        examples = {
            "uid": "YdMCHYy1MlPLnn4HEHFgNmf6MrE2",
            "avatar": "https://daangn-market.s3.amazonaws.com/media/avatars/carrot.jpeg",
            "phone": "+821022223333",
            "created": "2020-04-17T20:14:15.286093+09:00",
            "updated": "2020-04-17T20:14:15.370422+09:00",
            "username": "test-user",
            "Authorization": "Token abf88bad2c296ce6db376fd25d31304709215467"
        }

    def get_authorization(self, obj):
        return f'Token {obj.auth_token}'


# 로그인
class IdTokenSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate(self, attrs):
        # exceptions
        try:
            decoded = fb_auth.verify_id_token(attrs['id_token'])
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return decoded

    def to_representation(self, instance):
        return instance


# 회원 가입
class SignUpSerializer(IdTokenSerializer):
    id_token = serializers.CharField()
    username = serializers.CharField()
    avatar = serializers.ImageField(required=False)

    def validate(self, attrs):
        data = super(SignUpSerializer, self).validate({'id_token': attrs['id_token']})
        data['username'] = attrs['username']
        avatar = attrs.get('avatar', None)
        if avatar:
            data['avatar'] = avatar
        return data

    def to_representation(self, instance):
        return instance


# 내 동네 설정
class SetLocateSerializer(serializers.ModelSerializer):
    locate = LocateSerializer(read_only=True)

    def validate(self, attrs):
        instance = SelectedLocation(**attrs)
        instance.full_clean()
        return attrs

    def to_representation(self, instance):
        ret = super(SetLocateSerializer, self).to_representation(instance)
        ret['user'] = instance.user.username
        return ret

    def to_internal_value(self, data):
        data['user'] = self.context['request'].user
        location = Locate.objects.get(pk=data['locate'])
        data['locate'] = location
        return data

    class Meta:
        model = SelectedLocation
        fields = ('user', 'locate', 'distance', 'verified', 'activated')
        examples = {
            'user': 'test-user',
            'distance': '1000',
        }
