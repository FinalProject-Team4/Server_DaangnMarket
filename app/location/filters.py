from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter

from location.models import Locate


class LocationFilter(FilterSet):
    dong_id = CharFilter(
        field_name='pk', lookup_expr='exact', required=True, help_text='동 ID')
    distance = CharFilter(
        method='filter_distance', required=True, help_text='범위')

    class Meta:
        model = Locate
        fields = ['dong_id', 'distance']

    def filter_distance(self, qs, name, value):
        pnt = qs.get().latlng
        distance = self.data['distance']
        ret = Locate.objects.filter(
            latlng__distance_lt=(pnt, D(m=distance)),
        ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')
        return ret


class LocationSearchFilter(FilterSet):
    id = CharFilter(
        field_name='pk', lookup_expr='exact', help_text='동 ID')
    dong = CharFilter(
        field_name='dong', lookup_expr='icontains', help_text='동 이름')
    gu = CharFilter(
        field_name='gu', lookup_expr='icontains', help_text='구 이름')
    address = CharFilter(
        field_name='address', lookup_expr='icontains', help_text='도로명 주소')

    class Meta:
        model = Locate
        fields = ['id', 'dong', 'gu', 'address']
