from django.urls import path

from location.views import LocationListAPI, LocationSearchPI

app_name = "location"
urlpatterns = [
    path('', LocationListAPI.as_view()),
    path('search/', LocationSearchPI.as_view()),
]
