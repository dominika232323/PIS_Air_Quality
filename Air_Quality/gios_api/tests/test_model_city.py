import pytest

from gios_api.models import Province, District, Commune, City


@pytest.fixture
def city():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    return City.objects.create(commune=commune, name="city")


@pytest.mark.django_db
def test_model_creation(city):
    assert city.name == "city"


@pytest.mark.django_db
def test_model_string(city):
    assert str(city) == f"city in commune ({city.id})"
