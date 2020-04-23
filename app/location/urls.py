from django.urls import path

from location.views import LocationAPI, LocationSearchAPI

app_name = "location"
urlpatterns = [
    path('', LocationAPI.as_view()),
    path('search/', LocationSearchAPI.as_view()),
]
