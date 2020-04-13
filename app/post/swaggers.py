from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.swagger_custom import ExampleInspector
from post.serializers import PostImageUploadSerializer
from post.views import *

# 상품 이미지 업로드
decorated_post_image_upload_api = \
    swagger_auto_schema(
        # operation_description="게시물 업로드 API",
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['post_id', 'photos'],
            properties={
                'post_id': openapi.Schema(
                    description='게시물 번호',
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
        field_inspectors=[ExampleInspector],
        security=[],
        tags=['post'],
    )(ApiPostImageUpload.as_view())
