from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

class District(models.Model):
    name = models.CharField(max_length=100)
    commune_id = models.ForeignKey(Province)

class Commune(models.Model):
    name = models.CharField(max_length=100)
    commune_id = models.ForeignKey(District)

class City(models.Model):
    name = models.CharField(max_length=100)
    commune_id = models.ForeignKey(Commune)

class Address(models.Model):
    name = models.CharField(max_length=255)
    city_id = models.ForeignKey(City)

class Station(models.Model):
    station_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address_id = models.ForeignKey(Address)

class Parameter(models.Model):
    name = models.CharField(max_length=255)
    formula = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

class Sensor(models.Model):
    station_id = models.ForeignKey(Station)
    parameter = models.ForeignKey(Parameter)

class Measurement(models.Model):
    date = models.DateField()
    value = models.FloatField()
    param_code = models.ForeignKey(Parameter)
    sensor = models.ForeignKey(Sensor)
