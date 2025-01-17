from rest_framework import serializers
from .models import (
    Province, District, Commune, City, Address, Station, Parameter, Sensor,
    Measurement, AirQualityLevel, AirQuality, AirQualityPollutant
)

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer(read_only=True)

    class Meta:
        model = District
        fields = '__all__'


class CommuneSerializer(serializers.ModelSerializer):
    district = DistrictSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    commune = CommuneSerializer(read_only=True)

    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'


class StationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Station
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class SensorSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)
    parameter = ParameterSerializer(read_only=True)

    class Meta:
        model = Sensor
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    param_code = ParameterSerializer(read_only=True)
    sensor = SensorSerializer(read_only=True)

    class Meta:
        model = Measurement
        fields = '__all__'


class AirQualityLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualityLevel
        fields = '__all__'


class AirQualitySerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)
    quality_level = AirQualityLevelSerializer(read_only=True)

    class Meta:
        model = AirQuality
        fields = '__all__'


class AirQualityPollutantSerializer(serializers.ModelSerializer):
    air_quality = AirQualitySerializer(read_only=True)
    parameter = ParameterSerializer(read_only=True)
    quality_level = AirQualityLevelSerializer(read_only=True)

    class Meta:
        model = AirQualityPollutant
        fields = '__all__'
