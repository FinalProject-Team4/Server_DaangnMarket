from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(use_url=False, allow_empty_file=True)
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
