from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

class District(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Province)

class Commune(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(District)

class City(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune)

class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City)

class Station(models.Model):
    station_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.ForeignKey(Address)

class Parameter(models.Model):
    name = models.CharField(max_length=255)
    formula = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

class Sensor(models.Model):
    station = models.ForeignKey(Station)
    parameter = models.ForeignKey(Parameter)

class Measurement(models.Model):
    date = models.DateField()
    value = models.FloatField()
    param_code = models.ForeignKey(Parameter)
    sensor = models.ForeignKey(Sensor)

class AirQualityLevel(models.Model):
    level_name = models.CharField(max_length=50)

class AirQuality(models.Model):
    station = models.ForeignKey(Station)
    calculate_date = models.DateField()
    quality_level = models.IntegerField()
    source_date = models.DateField()
    index_status = models.BooleanField()
    critical_param = models.CharField(max_length=50)

class AirQualityPollutant(models.Model):
    air_quality = models.ForeignKey(AirQuality)
    parameter = models.ForeignKey(Parameter)
    calculate_date = models.DateField()
    quality_level = models.ForeignKey(AirQualityLevel)
    source_date = models.DateField()