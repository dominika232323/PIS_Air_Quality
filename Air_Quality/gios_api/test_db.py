import pytest
from gios_api.models import Sensor, Parameter, Measurement
from datetime import date, timedelta
from gios_api.services import check_db_for_measurements_in_period


@pytest.fixture()
def test_populate_sensor_readings(db):
    sensor_param = Parameter.objects.create(name = "test param")
    sensor_created = Sensor.objects.create(
        station = None,
        external_sensor_id = "001",
        parameter = sensor_param
    )
    sensor_measurements = [ (date.today()- timedelta(days = x), x) for x in range(0,30) ]
    for mes in sensor_measurements:
        Measurement.objects.create(
            sensor=sensor_created,
            date=mes[0],
            defaults= {
                'value': mes[1],
                'parameter': sensor_param,
            }
        )
    assert len(Measurement.objects.all()) == 30

# @pytest.mark.django_db
def test_get_data_week(db):
    # populate_sensor_readings()
    measurements_list = check_db_for_measurements_in_period("001", date.today().strftime('%Y-%m-%d %H:%M'), (date.today() - timedelta(days = 7)).strftime('%Y-%m-%d %H:%M'))
    assert len(measurements_list) == 7
    for mes, i in enumerate(measurements_list):
        assert mes.value == i
        assert mes.date == date.today() - timedelta(days = 7)
