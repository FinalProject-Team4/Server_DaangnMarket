from django.urls import path

from notification import views

urlpatterns = [
    path('register/', views.ApiFcmDeviceRegister.as_view()),
    path('send/', views.ApiSendFcm.as_view()),
]