from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# 게시글 생성, 수정
from rest_framework.permissions import IsAuthenticated

decorated_post_create_update_api = \
    swagger_auto_schema(
        consumes='multipart/form-data',
        permission_classes=[IsAuthenticated],

    )
