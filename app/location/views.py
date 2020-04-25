from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from config.c import LargeResultsSetPagination
from location.filters import LocationFilter, LocationRangeFilter
from location.models import Locate
from location.serializers import LocateSerializer, LocationDistanceSerializer


class LocationRangeAPI(ListAPIView):
    """
    기준 거리 범위에 있는 동 리스트

    (+ dong_id, [+lati, +longi])
    ### GET _/location/range/_
    """
    queryset = Locate.objects.all()
    serializer_class = LocationDistanceSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = LocationRangeFilter
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
