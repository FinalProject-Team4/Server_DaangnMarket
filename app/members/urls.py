from django.urls import path
from .views import *

app_name = "members"
urlpatterns = [
    # 테스트 클라이언드 사이드
    path("front/", entry_view, name="front"),
    path("signup/", signup_view, name="signup"),
    # API
    path("entry/", Entry.as_view(), name="entry"),
]
