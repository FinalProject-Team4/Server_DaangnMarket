import os

import firebase_admin
from firebase_admin import auth, credentials
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from location.models import Locate
from members.models import SelectedLocation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

cred = credentials.Certificate(f"{ROOT_DIR}/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

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
            decoded = auth.verify_id_token(attrs['id_token'])
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
    class Meta:
        model = SelectedLocation
        fields = ('user', 'locate', 'distance', 'verified', 'activated')
        examples = {
            'user': 'test-user',
            'locate': '6041',
            'distance': '1000',
        }

    def validate(self, attrs):
        instance = SelectedLocation(**attrs)
        instance.clean()
        return attrs
