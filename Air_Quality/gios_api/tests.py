import pytest
from django.urls import reverse
from gios_api.services import map_station_json_to_object, get_all_stations, get_station_sensors, map_sensor_json_to_object

def test_map_station_json_into_object():
    station_json = {
      "Identyfikator stacji": 77,
      "Kod stacji": "DsPolKasztan",
      "Nazwa stacji": "Polkowice, ul. Kasztanowa",
      "WGS84 φ N": "51.502370",
      "WGS84 λ E": "16.075051",
      "Identyfikator miasta": 721,
      "Nazwa miasta": "Polkowice",
      "Gmina": "Polkowice",
      "Powiat": "polkowicki",
      "Województwo": "DOLNOŚLĄSKIE",
      "Ulica": "ul. Kasztanowa 29"
    }

    station_data = map_station_json_to_object(station_json)
    assert station_data.id == 77
    assert station_data.name == 'Polkowice, ul. Kasztanowa'
    assert station_data.location.city == 'Polkowice'
    assert station_data.location.commune == 'Polkowice'
    assert station_data.location.district == 'polkowicki'
    assert station_data.location.voivodeship == 'DOLNOŚLĄSKIE'
    assert station_data.location.street == 'ul. Kasztanowa 29'


def test_get_all_stations():
    stations = get_all_stations()
    assert len(stations) > 0

def test_map_sensor_json_into_object():
    sensor_json = {
      "Identyfikator stanowiska": 464,
      "Identyfikator stacji": 77,
      "Wskaźnik": "kadm w PM10",
      "Wskaźnik - wzór": "Cd(PM10)",
      "Wskaźnik - kod": "Cd(PM10)",
      "Id wskaźnika": 57
    }
    sensor_data = map_sensor_json_to_object(sensor_json)
    assert sensor_data.id == 464
    assert sensor_data.indicator == 'kadm w PM10'


def test_get_station_sensors():
    sensors = get_station_sensors(77)
    assert len(sensors) == 6


