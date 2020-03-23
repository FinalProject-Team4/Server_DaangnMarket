from django.urls import path

from location import views

urlpatterns = [
    path('locate/', views.LocateListAPI.as_view()),
    path('locate/search/', views.SearchLocateAPI.as_view()),
    path('locate/gps/', views.GPSLocateAPI.as_view()),
]
