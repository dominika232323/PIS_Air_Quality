import pytest

from gios_api.models import Province, District


@pytest.fixture
def district():
    province = Province.objects.create(name="province")
    return District.objects.create(province=province, name="district")


@pytest.mark.django_db
def test_model_creation(district):
    assert district.name == "district"


@pytest.mark.django_db
def test_model_string(district):
    assert str(district) == f"district in province ({district.id})"
