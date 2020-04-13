from django.contrib.gis.db.models.functions import Distance

from django.contrib.gis.geos import Point
from rest_framework import generics, status

from django.contrib.gis.measure import D
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from config.c import LargeResultsSetPagination
from location.models import Locate
from location.serializers import LocateSerializer, DongSerializer


class LocateListAPI(generics.ListAPIView):
    '''
    동 ID값을 기준 거리 범위에 있는 동 리스트

    ## /locatoin/locate/
    ## Parameters
        - dong_id: 동 ID값
        - distance: 거리 설정(default:1000)
    ## 내용
        - id: 동 ID 값
        - dong: 동 이름
        - gu: 구 이름
        - longitude: 경도 값
        - latitude: 위도 값
        - address: 도로명 주소
        - distance: 검색한 동과의 거리 값
    '''
    pagination_class = LargeResultsSetPagination
    serializer_class = LocateSerializer

    def get_queryset(self):
        dong_id = self.request.query_params.get('dong_id', 0)
        distance = self.request.query_params.get('distance', 1000)
        try:
            dong = Locate.objects.get(id=dong_id)
        except Locate.DoesNotExist:
            print('Locate.DoesNotExist')
            raise ValidationError(['There are no dong_id'])

        pnt = dong.latlng
        locates = Locate.objects.filter(
            latlng__distance_lt=(pnt, D(m=distance)),
        ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')
        return locates


class SearchLocateAPI(generics.ListAPIView):
    '''
    동 검색

    ---
    ## /location/locate/
    ## Parameters
        - dong_name: 동 이름
    ## 내용
        - id: 동 ID 값
        - dong: 동 이름
        - gu: 구 이름
        - longitude: 경도 값
        - latitude: 위도 값
        - address: 도로명 주소
    '''
    pagination_class = LargeResultsSetPagination
    serializer_class = DongSerializer

    def get_queryset(self):
        dong_name = self.request.query_params.get('dong_name', '')

        locate_list = Locate.objects.filter(dong__contains=dong_name)
        return locate_list


class GPSLocateAPI(generics.ListAPIView):
    '''
    동 위도, 경도 값을 기준 거리 범위에 있는 동 리스트

    ---
    ## /locatoin/locate/gps/
    ## Parameters
        - longtitude: 위도 값
        - latitude: 경도 값
        - distance: 거리 설정(default:1000)
    ## 내용
        - id: 동 ID 값
        - dong: 동 이름
        - gu: 구 이름
        - longitude: 경도 값
        - latitude: 위도 값
        - address: 도로명 주소
        - distance: 검색한 동과의 거리 값
    '''
    pagination_class = LargeResultsSetPagination
    serializer_class = LocateSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude', 0)
        longitude = self.request.query_params.get('longitude', 0)
        distance = self.request.query_params.get('distance', 1000)

        pnt = Point(float(longitude), float(latitude))
        locates = Locate.objects.filter(
            latlng__distance_lt=(pnt, D(m=distance)),
        ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')

        return locates
