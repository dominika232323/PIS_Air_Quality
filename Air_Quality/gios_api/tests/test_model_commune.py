import pytest

from gios_api.models import Province, District, Commune


@pytest.fixture
def commune():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    return Commune.objects.create(district=district, name="commune")


@pytest.mark.django_db
def test_model_creation(commune):
    assert commune.name == "commune"


@pytest.mark.django_db
def test_model_string(commune):
    assert str(commune) == f"commune in district ({commune.id})"
