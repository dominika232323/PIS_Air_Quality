from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL)

class Commune(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.SET_NULL)

class City(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.SET_NULL)

class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL)

class Station(models.Model):
    station_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.SET_NULL)

class Parameter(models.Model):
    name = models.CharField(max_length=255)
    formula = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

class Sensor(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL)
    parameter = models.ForeignKey(Parameter, on_delete=models.SET_NULL)

class Measurement(models.Model):
    date = models.DateField()
    value = models.FloatField()
    param_code = models.ForeignKey(Parameter, on_delete=models.SET_NULL)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL)

class AirQualityLevel(models.Model):
    level_name = models.CharField(max_length=50)

class AirQuality(models.Model):
    station = models.ForeignKey(Station, on_delete=models.SET_NULL)
    calculate_date = models.DateField()
    quality_level = models.ForeignKey(AirQualityLevel, on_delete=models.SET_NULL)
    source_date = models.DateField()
    index_status = models.BooleanField()
    critical_param = models.CharField(max_length=50)

class AirQualityPollutant(models.Model):
    air_quality = models.ForeignKey(AirQuality, on_delete=models.SET_NULL)
    parameter = models.ForeignKey(Parameter ,on_delete=models.SET_NULL)
    calculate_date = models.DateField()
    quality_level = models.ForeignKey(AirQualityLevel ,on_delete=models.SET_NULL)
    source_date = models.DateField()