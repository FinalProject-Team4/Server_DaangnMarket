from django.urls import path

from chat import views

urlpatterns = [
    path('room/save/', views.ApiRoomSave.as_view()),
    path('room/list/', views.ApiRoomList.as_view()),
    path('message/save/', views.ApiMessageSave.as_view()),
    path('room/messages/', views.ApiMessageList.as_view()),
]