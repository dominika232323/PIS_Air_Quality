import pytest

from gios_api.models import Province, District, Commune, City, Address


@pytest.fixture
def address():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    return Address.objects.create(city=city, name="address")


@pytest.mark.django_db
def test_model_creation(address):
    assert address.name == "address"


@pytest.mark.django_db
def test_model_string(address):
    assert str(address) == f"address in city ({address.id})"
