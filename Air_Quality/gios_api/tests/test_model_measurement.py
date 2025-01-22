from datetime import datetime

import pytest

from gios_api.models import Province, Parameter, Sensor, Station, Address, City, Commune, District, Measurement


@pytest.fixture
def measurement():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    station = Station.objects.create(address=address, station_name="station", external_station_id="123")

    param = Parameter.objects.create(name="param")
    sensor = Sensor.objects.create(parameter=param, station=station, external_sensor_id="456")

    now = datetime.now()

    return now, Measurement.objects.create(sensor=sensor, parameter=param, value=12.5, date=now)


@pytest.mark.django_db
def test_model_creation(measurement):
    assert measurement[1].date == measurement[0]
    assert measurement[1].value == 12.5


@pytest.mark.django_db
def test_model_string(measurement):
    assert str(measurement[1]) == f"Measured 12.5 for {measurement[1].parameter.name} on {measurement[1].date} ({measurement[1].id})"

