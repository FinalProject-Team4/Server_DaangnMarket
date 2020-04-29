from django.urls import path

from location.views import LocationAPI, LocationRangeAPI

app_name = "location"
urlpatterns = [
    path('', LocationAPI.as_view()),
    path('range/', LocationRangeAPI.as_view()),
]
