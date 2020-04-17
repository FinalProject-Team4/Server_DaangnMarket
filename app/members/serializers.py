import os

import firebase_admin
from firebase_admin import auth, credentials
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

cred = credentials.Certificate(f"{ROOT_DIR}/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

User = get_user_model()


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

    def get_authorization(self, obj):
        return f'Token {obj.auth_token}'


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
