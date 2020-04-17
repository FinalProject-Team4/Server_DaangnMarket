from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.swagger_custom import MyAutoSchema
from members.serializers import UserSerializer

decorated_login_api = \
    swagger_auto_schema(
        request_body=openapi.Sc
    )

decorated_signup_api = \
    MyAutoSchema(
        # operation_description="Login API",
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['idToken', 'username'],
            properties={
                'idToken': openapi.Schema(
                    description='Firbase Token',
                    type=openapi.TYPE_STRING
                ),
                'username': openapi.Schema(
                    description='Nickname',
                    type=openapi.TYPE_STRING
                ),
                # 'avatar': openapi.Schema(
                #     description='Profile Image',
                #     type=openapi.TYPE_FILE
                # )
            }
        ),
        responses={
            200: openapi.Response(
                description='success',
                examples={
                    'application/json': {
                        'uid': 'DadTiDdhiud2lxIlUmnXPCikvGL2',
                        'avatar': 'http://image.server/avatar/test-user-filename.jpg',
                        'phone': '+821044445555',
                        'created': '2020-04-01T17:37:43.034590+09:00',
                        'updated': '2020-04-01T17:37:43.034590+09:00',
                        # 'username': 'test-user',
                        'Authorization': 'Token 12603947067786edef122d86b9b4051d2115bade',
                    }
                },
                schema=UserSerializer
            ),
            401: openapi.Response(
                description='failed',
            )
        },
        security=[],
        tags=['Users'],
    )(SignUp.as_view())
# MyAutoSchema(
#     # operation_description="Signup API",
#     method='post',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         required=['idToken', 'username'],
#         properties={
#             'idToken': openapi.Schema(
#                 description='Firbase Token',
#                 type=openapi.TYPE_STRING
#             ),
#             'username': openapi.Schema(
#                 description='Nickname',
#                 type=openapi.TYPE_STRING
#             ),
#             'avatar': openapi.Schema(
#                 description='Profile Image',
#                 type=openapi.TYPE_FILE
#             )
#         }
#     ),
#     responses={
#         200: openapi.Response(
#             description='success',
#             examples={
#                 'application/json': {
#                     'uid': 'DadTiDdhiud2lxIlUmnXPCikvGL2',
#                     'avatar': 'http://image.server/avatar/test-user-filename.jpg',
#                     'phone': '+821044445555',
#                     'created': '2020-04-01T17:37:43.034590+09:00',
#                     'updated': '2020-04-01T17:37:43.034590+09:00',
#                     'username': 'test-user',
#                     'Authorization': 'Token 12603947067786edef122d86b9b4051d2115bade',
#                 }
#             },
#             schema=UserSerializer
#         ),
#     },
#     security=[],
#     tags=['Users'],
# )(SignUp.as_view())
