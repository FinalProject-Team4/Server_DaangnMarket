from django.urls import path

from post.views import (
    PostListAPI,
    PostLikeSave,
    PostDetailAPI,
    SearchAPI,
    SearchSaveAPI,
    PostLikeList,
    PostCreateUpdateDestroy)

app_name = 'post'
urlpatterns = [
    path('', PostCreateUpdateDestroy.as_view({
        'post': 'create',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('list/', PostListAPI.as_view()),
    path('detail/', PostDetailAPI.as_view()),

    path('search/', SearchAPI.as_view()),
    path('search/save/', SearchSaveAPI.as_view()),
    path('like/', PostLikeSave.as_view()),
    path('like/list/', PostLikeList.as_view()),
]
