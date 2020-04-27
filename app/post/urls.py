from django.urls import path

from post.views import (
    PostListAPI,
    PostLikeSave,
    PostDetailAPI,
    PostCreateAPI,
    SearchAPI,
    SearchSaveAPI,
    PostLikeList,
    ApiPostUpdate,
)

app_name = 'post'
urlpatterns = [
    path('list/', PostListAPI.as_view()),
    path('detail/', PostDetailAPI.as_view()),
    path('create/', PostCreateAPI.as_view()),

    # 판매 상품 상태 변경
    path('update/', ApiPostUpdate.as_view()),
    path('search/', SearchAPI.as_view()),
    path('search/save/', SearchSaveAPI.as_view()),
    path('like/', PostLikeSave.as_view()),
    path('like/list/', PostLikeList.as_view()),
]
