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
