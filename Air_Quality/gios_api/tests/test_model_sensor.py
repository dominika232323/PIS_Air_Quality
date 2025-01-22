import pytest

from gios_api.models import Province, Parameter, Sensor, Station, Address, City, Commune, District


@pytest.fixture
def sensor():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    station = Station.objects.create(address=address, station_name="station", external_station_id="123")

    param = Parameter.objects.create(name="param")

    return Sensor.objects.create(parameter=param, station=station, external_sensor_id="456")


@pytest.mark.django_db
def test_model_creation(sensor):
    assert sensor.external_sensor_id == "456"


@pytest.mark.django_db
def test_model_string(sensor):
    assert str(sensor) == f"Sensor 456 at station measuring param ({sensor.id})"


@pytest.fixture
def sensor_external_none():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    station = Station.objects.create(address=address, station_name="station", external_station_id="123")

    param = Parameter.objects.create(name="param")

    return Sensor.objects.create(parameter=param, station=station)


@pytest.mark.django_db
def test_model_creation(sensor_external_none):
    assert sensor_external_none.external_sensor_id is None


@pytest.mark.django_db
def test_model_string(sensor_external_none):
    assert str(sensor_external_none) == f"Sensor at station measuring param ({sensor_external_none.id})"
