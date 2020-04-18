from django.urls import path

from post.views import *

app_name = 'post'
urlpatterns = [
    # path('locate/', LocateListAPI.as_view()),
    path('list/', ApiPostList.as_view()),
    path('list/gps/', ApiPostListWithGPS.as_view()),
    path('list/category/', ApiPostListWithCate.as_view()),
    path('detail/', ApiPostDetail.as_view()),
    path('create/', ApiPostCreate.as_view()),
    path('create/locate/', ApiPostCreateLocate.as_view()),
    path('image/upload/', PostImageUploadAPI.as_view()),
    path('search/', SearchAPI.as_view()),
]
