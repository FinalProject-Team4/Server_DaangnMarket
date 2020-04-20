from django.urls import path

from location.views import LocationListAPI, LocationSearchPI

urlpatterns = [
    path('', LocationListAPI.as_view()),
    path('search/', LocationSearchPI.as_view()),
]
