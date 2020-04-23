from django.urls import path

from location.views import LocationAPI, LocationDongDistanceSearchAPI, LocationLatLngDistanceSearchAPI

app_name = "location"
urlpatterns = [
    path('', LocationAPI.as_view()),
    path('distance/dong/', LocationDongDistanceSearchAPI.as_view()),
    path('distance/latlng/', LocationLatLngDistanceSearchAPI.as_view()),
]
