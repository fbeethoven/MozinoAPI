from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import provider, area

class providerSerializer(ModelSerializer):
    class Meta:
        model = provider
        fields = '__all__'


class areaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = area
        geo_field = "service_area"
        fields = '__all__'
