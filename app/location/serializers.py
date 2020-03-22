from rest_framework import serializers

from location.models import Locate


class LocateSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return obj.distance.m

    class Meta:
        model = Locate
        fields = (
            'id', 'dong', 'gu', 'longitude', 'latitude', 'address', 'distance'
        )


