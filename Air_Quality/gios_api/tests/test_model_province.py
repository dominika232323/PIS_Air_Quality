import pytest

from gios_api.models import Province


@pytest.fixture
def province():
    return Province.objects.create(name="province")


@pytest.mark.django_db
def test_model_creation(province):
    assert province.name == "province"


@pytest.mark.django_db
def test_model_string(province):
    assert str(province) == f"province ({province.id})"
