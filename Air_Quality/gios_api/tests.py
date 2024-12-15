import pytest
from django.urls import reverse
from gios_api.services import (map_station_json_to_object, get_all_stations,
                               get_station_sensors, map_sensor_json_to_object,
                               get_current_sensor_measurements)
import requests


def test_map_station_json_into_object():
    station_json = {
        "id": 114,
        "stationName": "Wrocław, ul. Bartnicza",
        "gegrLat": "51.115933",
        "gegrLon": "17.141125",
        "city": {
            "id": 1064,
            "name": "Wrocław",
            "commune": {
                "communeName": "Wrocław",
                "districtName": "Wrocław",
                "provinceName": "DOLNOŚLĄSKIE"
            }
            },
        "addressStreet": "ul. Bartnicza"
    }

    station_data = map_station_json_to_object(station_json)
    assert station_data.id == 114
    assert station_data.name == 'Wrocław, ul. Bartnicza'
    assert station_data.location.city == 'Wrocław'
    assert station_data.location.commune == 'Wrocław'
    assert station_data.location.district == 'Wrocław'
    assert station_data.location.voivodeship == 'DOLNOŚLĄSKIE'
    assert station_data.location.street == 'ul. Bartnicza'


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


def test_get_sensor_measurements():
    measurements = get_current_sensor_measurements(52)
    assert measurements[1].date is not None
    assert measurements[1].value is not None


def test_get_all_stations_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")

    monkeypatch.setattr(requests, "get", mock_get)

    result = get_all_stations()
    assert result == []


def test_get_all_sensors_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")

    monkeypatch.setattr(requests, "get", mock_get)

    result = get_station_sensors(55)
    assert result == []


def test_get_current_station_mesurements_execption(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")

    monkeypatch.setattr(requests, "get", mock_get)

    result = get_current_sensor_measurements(55)
    assert result == []
