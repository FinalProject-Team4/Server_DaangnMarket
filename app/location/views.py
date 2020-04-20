from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from config.c import LargeResultsSetPagination
from location.filters import LocationFilter, LocationSearchFilter
from location.models import Locate
from location.serializers import LocateSerializer, LocationDistanceSerializer


class LocationListAPI(ListAPIView):
    """
    동 ID값을 기준 거리 범위에 있는 동 리스트

    ### GET _/location/_
    """
    queryset = Locate.objects.all()
    serializer_class = LocationDistanceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = LocationFilter
    ordering = ('-distance',)
    pagination_class = LargeResultsSetPagination


class LocationSearchPI(ListAPIView):
    '''
    주소 리스트 검색

    (+ 동 ID, + 동 이름, + 구 이름, + 도로명 주소)
    ### GET _/location/locate/_
    '''
    queryset = Locate.objects.all()
    filter_class = LocationSearchFilter
    serializer_class = LocateSerializer
    pagination_class = LargeResultsSetPagination
