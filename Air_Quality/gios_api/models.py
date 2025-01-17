from django.db import models

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = "provinces"


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.province.name}"

    class Meta:
        managed = False
        db_table = "districts"


class Commune(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.district.name}"

    class Meta:
        managed = False
        db_table = "communes"


class City(models.Model):
    name = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.commune.name}"

    class Meta:
        managed = False
        db_table = "cities"


class Address(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} in {self.city.name}"

    class Meta:
        managed = False
        db_table = "addresses"


class Station(models.Model):
    station_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.station_name} at ({self.latitude}, {self.longitude}) in {self.address.name}"

    class Meta:
        managed = False
        db_table = "stations"


class Parameter(models.Model):
    name = models.CharField(max_length=255)
    formula = models.CharField(max_length=50)
    code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} (Formula: {self.formula}, Code: {self.code})"

    class Meta:
        managed = False
        db_table = "params"


class Sensor(models.Model):
    station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
    parameter = models.ForeignKey(Parameter, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Sensor at {self.station.station_name} measuring {self.parameter.name}"

    class Meta:
        managed = False
        db_table = "sensors"


class Measurement(models.Model):
    date = models.DateField()
    value = models.FloatField()
    param_code = models.ForeignKey(Parameter, null=True, on_delete=models.SET_NULL)
    sensor = models.ForeignKey(Sensor, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.value} for {self.param_code.name} on {self.date}"

    class Meta:
        managed = False
        db_table = "measurements"


class AirQualityLevel(models.Model):
    level_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.level_name}"

    class Meta:
        managed = False
        db_table = "air_quality_levels"


class AirQuality(models.Model):
    station = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL)
    calculate_date = models.DateField()
    quality_level = models.ForeignKey(AirQualityLevel, null=True, on_delete=models.SET_NULL)
    source_date = models.DateField()
    index_status = models.BooleanField()
    critical_param = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.quality_level.level_name} at {self.station} on {self.calculate_date}: "

    class Meta:
        managed = False
        db_table = "air_quality"


class AirQualityPollutant(models.Model):
    air_quality = models.ForeignKey(AirQuality, null=True, on_delete=models.SET_NULL)
    parameter = models.ForeignKey(Parameter ,null=True, on_delete=models.SET_NULL)
    calculate_date = models.DateField()
    quality_level = models.ForeignKey(AirQualityLevel ,null=True, on_delete=models.SET_NULL)
    source_date = models.DateField()

    def __str__(self):
        return f"{self.parameter} for {self.air_quality.station.station_name} at {self.calculate_date} "

    class Meta:
        managed = False
        db_table = "air_quality_pollutants"
