from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from config.c import LargeResultsSetPagination
from location.filters import LocationDistanceFilter, LocationFilter, LocationLatLngFilter
from location.models import Locate
from location.serializers import LocateSerializer, LocationDistanceSerializer


class LocationDongDistanceSearchAPI(ListAPIView):
    """
    동 ID값을 기준 거리 범위에 있는 동 리스트

    ### GET _/location/distance/dong/_
    """
    queryset = Locate.objects.all()
    serializer_class = LocationDistanceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = LocationDistanceFilter
    ordering = ('-distance',)
    pagination_class = LargeResultsSetPagination


class LocationLatLngDistanceSearchAPI(ListAPIView):
    """
    위도 경도 값을 기준 거리 범위에 있는 동 리스트

    ### GET _/location/distance/latlng/_
    """
    queryset = Locate.objects.all()
    serializer_class = LocationDistanceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = LocationLatLngFilter
    ordering = ('-distance',)
    pagination_class = LargeResultsSetPagination


class LocationAPI(ListAPIView):
    """
    주소 리스트 검색

    (+ 동 ID, + 동 이름, + 구 이름, + 도로명 주소)
    ### GET _/location/_
    """
    queryset = Locate.objects.all()
    filter_class = LocationFilter
    serializer_class = LocateSerializer
    pagination_class = LargeResultsSetPagination
