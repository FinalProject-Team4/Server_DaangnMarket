from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from post.views import *

# 상품 이미지 업로드
decorated_post_image_upload_api = \
    swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['post_id', 'photos'],
            properties={
                'post_id': openapi.Schema(
                    description='게시글 번호',
                    type=openapi.TYPE_INTEGER
                ),
                'photos': openapi.Schema(
                    description='상품 이미지 [`file1`, `file2` , ...]',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                    )
                )
            },
        ),
        consumes='multipart/form-data',

        responses={
            201: openapi.Response(
                description='Success',
                schema=PostImageUploadSerializer,
            ),
            400: openapi.Response(
                description='Bad Request',
            )
        },
        tags=['post'],
    )

# 게시글 생성
decorated_post_create_api = \
    swagger_auto_schema(
        consumes='multipart/form-data',
    )
