from django.contrib.gis.db.models.functions import Distance

from rest_framework import generics

from django.contrib.gis.measure import D

from location.models import Locate
from location.serializers import LocateSerializer


class LocateListAPI(generics.ListAPIView):
    serializer_class = LocateSerializer

    def get_queryset(self):
        dong_id = self.request.query_params.get('dong_id', '0')
        distance = self.request.query_params.get('distance', 1000)
        dong = Locate.objects.get(id=dong_id)

        pnt = dong.latlng
        locates = Locate.objects.filter(
            latlng__distance_lt=(pnt, D(m=distance)),
        ).annotate(distance=Distance(pnt, 'latlng')).order_by('distance')

        return locates


