from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from members.serializers import UserSerializer

decorated_login_api = \
    swagger_auto_schema(
        responses={
            201: openapi.Response(
                description='Success',
                schema=UserSerializer,
            ),
        },
        tags=['Users'],
    )

decorated_signup_api = \
    swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id_token', 'username'],
            properties={
                'id_token': openapi.Schema(
                    description='파이어베이스 토큰',
                    type=openapi.TYPE_STRING
                ),
                'username': openapi.Schema(
                    description='닉네임',
                    type=openapi.TYPE_STRING
                ),
                'avatar': openapi.Schema(
                    description='프로필 사진',
                    type=openapi.TYPE_STRING
                ),
            }
        ),
        consumes='multipart/form-data',
        responses={
            201: openapi.Response(
                description='Success',
                schema=UserSerializer,
            ),
        },
        tags=['Users'],
    )