from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "provinces"


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.province.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "districts"


class Commune(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.district.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "communes"


class City(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.commune.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "cities"


class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.city.name} ({self.id})"

    class Meta:
        managed = True
        unique_together = ('name', 'city')
        db_table = "addresses"


class Station(models.Model):
    station_name = models.CharField(max_length=255)
    external_station_id = models.CharField(max_length=255, null=True, unique=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.external_station_id is not None:
            return f"{self.station_name} {self.external_station_id} on {self.address.name} ({self.id})"
        return f"{self.station_name} on {self.address.name} ({self.id})"


    class Meta:
        managed = True
        db_table = "stations"


class Parameter(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "params"


class Sensor(models.Model):
    station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
    external_sensor_id = models.CharField(max_length=255, null=True, unique=True)
    parameter = models.ForeignKey(Parameter, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.external_sensor_id is not None:
            return f"Sensor {self.external_sensor_id} at {self.station.station_name} measuring {self.parameter.name} ({self.id})"
        return f"Sensor at {self.station.station_name} measuring {self.parameter.name} ({self.id})"

    class Meta:
        managed = True
        db_table = "sensors"


class Measurement(models.Model):
    date = models.DateTimeField()
    value = models.FloatField()
    parameter = models.ForeignKey(Parameter, null=True, on_delete=models.SET_NULL)
    sensor = models.ForeignKey(Sensor, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Measured {self.value} for {self.parameter.name} on {self.date} ({self.id})"

    class Meta:
        managed = True
        db_table = "measurements"


class AirQualityLevel(models.Model):
    level_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.level_name} ({self.id})"

    class Meta:
        managed = True
        db_table = "air_quality_levels"


class AirQuality(models.Model):
    station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
    calculate_date = models.DateTimeField()
    air_quality_level = models.ForeignKey(AirQualityLevel, null=True, on_delete=models.SET_NULL)
    source_date = models.DateTimeField()
    index_status = models.BooleanField()
    critical_param = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.air_quality_level.level_name} at {self.station.station_name} on {self.source_date} ({self.id})"

    class Meta:
        managed = True
        db_table = "air_quality"


class AirQualityPollutant(models.Model):
    air_quality = models.ForeignKey(AirQuality, null=True, on_delete=models.SET_NULL)
    parameter = models.ForeignKey(Parameter ,null=True, on_delete=models.SET_NULL)
    calculate_date = models.DateTimeField()
    air_quality_level = models.ForeignKey(AirQualityLevel ,null=True, on_delete=models.SET_NULL)
    source_date = models.DateTimeField()

    def __str__(self):
        return f"{self.parameter} for {self.air_quality.station.station_name} at {self.source_date} ({self.id})"

    class Meta:
        managed = True
        db_table = "air_quality_pollutants"
