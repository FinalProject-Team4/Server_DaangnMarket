from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# 게시글 생성
decorated_post_create_api = \
    swagger_auto_schema(
        consumes='multipart/form-data',
    )
