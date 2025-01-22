import pytest

from gios_api.models import AirQualityLevel


@pytest.fixture
def air_quality_level():
    return AirQualityLevel.objects.create(level_name="good")


@pytest.mark.django_db
def test_model_creation(air_quality_level):
    assert air_quality_level.level_name == "good"


@pytest.mark.django_db
def test_model_string(air_quality_level):
    assert str(air_quality_level) == f"good ({air_quality_level.id})"
