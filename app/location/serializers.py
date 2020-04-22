from rest_framework import serializers

from location.models import Locate


class LocateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locate
        fields = (
            'id', 'dong', 'gu', 'longitude', 'latitude', 'address'
        )
        examples = {
            "id": 6971,
            "dong": "상도1동",
            "gu": "동작구",
            "longitude": "126.95308900",
            "latitude": "37.49810000",
            "address": "서울특별시 동작구 상도로53길 9"
        }


class LocationDistanceSerializer(LocateSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return obj.distance.m

    class Meta(LocateSerializer.Meta):
        model = Locate
        fields = LocateSerializer.Meta.fields + ('distance',)
