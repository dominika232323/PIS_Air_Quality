import pytest

from gios_api.models import Province, District, Commune, City, Address, Station


@pytest.fixture
def station():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    return Station.objects.create(address=address, station_name="station", external_station_id="123")


@pytest.mark.django_db
def test_model_creation(station):
    assert station.station_name == "station"
    assert station.external_station_id == "123"


@pytest.mark.django_db
def test_model_string(station):
    assert str(station) == f"station 123 on address ({station.id})"


@pytest.fixture
def station_external_none():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    return Station.objects.create(address=address, station_name="station")


@pytest.mark.django_db
def test_model_creation(station_external_none):
    assert station_external_none.station_name == "station"
    assert station_external_none.external_station_id is None


@pytest.mark.django_db
def test_model_string(station_external_none):
    assert str(station_external_none) == f"station on address ({station_external_none.id})"
