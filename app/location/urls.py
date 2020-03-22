from django.urls import path

from location import views

urlpatterns = [
    path('locate/', views.LocateListAPI.as_view()),
]