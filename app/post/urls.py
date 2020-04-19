from django.urls import path

from post.views import *

app_name = 'post'
urlpatterns = [
    path('list/', ApiPostList.as_view()),
    path('detail/', ApiPostDetail.as_view()),
    path('create/', ApiPostCreate.as_view()),
    path('create/locate/', ApiPostCreateLocate.as_view()),
    path('image/upload/', PostImageUploadAPI.as_view()),
    # TODO : viewset 으로 분리
    path('search/', SearchAPI.as_view()),
    path('search/save/', SearchSaveAPI.as_view()),
]
