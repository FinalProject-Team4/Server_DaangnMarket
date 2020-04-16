from django.urls import path

from post.views import *
from post.swaggers import *

urlpatterns = [
    # path('locate/', LocateListAPI.as_view()),
    path('list/', ApiPostList.as_view()),
    path('list/gps/', ApiPostListWithGPS.as_view()),
    path('list/category/', ApiPostListWithCate.as_view()),
    path('detail/', ApiPostDetail.as_view()),
    path('create/', ApiPostCreate.as_view()),
    path('create/locate/', ApiPostCreateLocate.as_view()),
    path('image/upload/', ApiPostImageUpload.as_view()),

    # 검색
    # path('search/', ApiSearch.as_view()),
]
