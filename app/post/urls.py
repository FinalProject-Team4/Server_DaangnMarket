from django.urls import path

from post import views

urlpatterns = [
    # path('locate/', views.LocateListAPI.as_view()),
    path('list/', views.ApiPostList.as_view()),
    path('list/gps/', views.ApiPostListWithGPS.as_view()),
    path('list/category/', views.ApiPostListWithCate.as_view()),
    path('detail/', views.ApiPostDetail.as_view()),
    path('create/', views.ApiPostCreate.as_view()),
    path('image/upload/', views.ApiPostImageUpload.as_view()),
]
