import pytest
from gios_api.models import Sensor, Parameter, Measurement, Station, Address, City, Commune, District, Province
from datetime import date, timedelta, datetime
from gios_api.db_services import check_db_for_measurements_in_period


@pytest.fixture()
def populate_sensor_readings(db):
    # cit = City.objects.create(name = "city")
    # addr = Address.objects.create(name = "address", city = cit)
    stat = Station.objects.create(station_name = "station", external_station_id= "001", address = None)
    sensor_param = Parameter.objects.create(name = "test param")
    sensor_created = Sensor.objects.create(
        station = stat,
        external_sensor_id = "001",
        parameter = sensor_param
    )
    Sensor.objects.create(
        station = stat,
        external_sensor_id = "52",
        parameter = sensor_param
    )
    sensor_measurements = [ (date.today()- timedelta(days = x), x) for x in range(0,30) ]
    for mes in sensor_measurements:
        Measurement.objects.create(
            sensor=sensor_created,
            date=mes[0],
            value=  mes[1],
            parameter =  sensor_param
        )
    assert len(Measurement.objects.all()) == 30

@pytest.mark.django_db
def test_get_data_week(populate_sensor_readings):
    # populate_sensor_readings()
    measurements_list = check_db_for_measurements_in_period("001", (date.today() - timedelta(days = 6)).strftime('%Y-%m-%d %H:%M'), date.today().strftime('%Y-%m-%d %H:%M'))
    assert len(measurements_list) == 7
    for i, mes in enumerate(measurements_list):
        assert mes.value == len(measurements_list) - (i+1)
        test_date = date.today() - timedelta(days = (len(measurements_list) -1-i))
        assert mes.date.date() == test_date

def test_non_existant_node(populate_sensor_readings):
    # populate_sensor_readings()
    measurements_list = check_db_for_measurements_in_period('002', '2025-01-01 15:00', '2025-01-10 15:00')
    assert len(measurements_list) == 0

def test_no_data_in_db(populate_sensor_readings):
    # populate_sensor_readings()
    measurements_list = check_db_for_measurements_in_period('52', '2025-01-01 15:00', '2025-01-10 15:00')
    assert len(measurements_list) >0