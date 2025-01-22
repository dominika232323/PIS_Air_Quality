import pytest

from gios_api.models import Province, Parameter


@pytest.fixture
def parameter():
    return Parameter.objects.create(name="param")


@pytest.mark.django_db
def test_model_creation(parameter):
    assert parameter.name == "param"


@pytest.mark.django_db
def test_model_string(parameter):
    assert str(parameter) == f"param ({parameter.id})"
