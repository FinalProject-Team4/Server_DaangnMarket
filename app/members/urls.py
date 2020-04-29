from django.urls import path
from .views import (
    entry_view, signup_view, LoginAPI, SignUpAPI, SetLocateAPI,
    UserInfoAPI)

app_name = "members"
urlpatterns = [
    # 테스트 클라이언드 사이드
    path("front/", entry_view, name="front"),
    path("front_signup/", signup_view, name="signup_front"),
    # API
    path("info/", UserInfoAPI.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name="info"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("signup/", SignUpAPI.as_view(), name="signup"),
    path("locate/", SetLocateAPI.as_view({
        'get': 'list',
        'post': 'create',
        'patch': 'partial_update',
        'delete': 'destroy',
    }), name="user_locations"),
]
