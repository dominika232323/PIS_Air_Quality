import pytest
from gios_api.errors import InvalidDateFormatError, TooWideDateRangeError
from django.urls import reverse
from gios_api.services import (map_station_json_to_object, get_all_stations,
                               get_station_sensors, map_sensor_json_to_object,
                               get_current_sensor_measurements, map_measurement_json_to_object,
                               get_archival_sensor_measurements, check_date_format,
                               check_date_wide, get_last_n_days_sensor_measurements,
                               get_current_station_air_quality)
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



def test_map_station_json_into_street_null():
    station_json ={
    "id": 612,
    "stationName": "Borsukowizna, Szkółka Leśna",
    "gegrLat": "53.215492",
    "gegrLon": "23.642153",
    "city": {
      "id": 63,
      "name": "Borsukowizna",
      "commune": {
        "communeName": "Krynki",
        "districtName": "sokólski",
        "provinceName": "PODLASKIE"
      }
    },
    "addressStreet": 'null'
  }

    station_data = map_station_json_to_object(station_json)
    assert station_data.location.city == 'Borsukowizna'

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

def test_map_mesurements_execption_bad_date():
    measurement = {
      "Kod stanowiska": "Whatever",
      "Data": "This is a very bad Date",
      "Wartość": 41.8
    }
    mes = map_measurement_json_to_object(measurement)
    assert mes.date is None
    assert mes.value == -1


def test_map_mesurements_execption_negative_value():
    measurement = {
      "Kod stanowiska": "Whatever",
      "Data": "2024-12-14 20:00:00",
      "Wartość": -58
    }
    mes = map_measurement_json_to_object(measurement)
    assert mes.date is None
    assert mes.value == -1


def test_map_mesurements_execption_null_value():
    measurement = {
      "Kod stanowiska": "Whatever",
      "Data": "2024-12-14 20:00:00",
      "Wartość": "null"
    }
    mes = map_measurement_json_to_object(measurement)
    assert mes.date is None
    assert mes.value == -1

def test_check_date_format_correct():
    check_date_format('2025-01-01 15:00')

def test_check_date_format_exception():
    with pytest.raises(InvalidDateFormatError, match='Invalid Date format! Expected Format: %Y-%m-%d %H:%M. Got: 12-01-2025 15:00'):
        check_date_format('12-01-2025 15:00')

def test_check_date_format_random_str():
    with pytest.raises(InvalidDateFormatError, match='Invalid Date format! Expected Format: %Y-%m-%d %H:%M. Got: 1234'):
        check_date_format('1234')

def test_reject_too_wide_date_range():
    with pytest.raises(TooWideDateRangeError):
        check_date_wide('2022-01-01 15:00', '2025-01-01 15:00', '%Y-%m-%d %H:%M')

def test_get_all_stations():
    stations = get_all_stations()
    assert len(stations) > 0


def test_get_station_sensors():
    sensors = get_station_sensors(77)
    assert len(sensors) == 6


def test_get_current_sensor_measurements():
    measurements = get_current_sensor_measurements(52)
    assert len(measurements) > 0

def test_get_archive_sensor_mesurements():
    measurements = get_archival_sensor_measurements(52, '2025-01-01 15:00', '2025-01-10 15:00')
    assert measurements[0].date.strftime('%Y-%m-%d %H:%M') == '2025-01-01 15:00'

def test_get_archive_sensor_mesurements_from_last_n_days():
    measurements = get_last_n_days_sensor_measurements(52, 7)
    assert len(measurements) > 0

def test_get_all_stations_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")
    monkeypatch.setattr(requests, "get", mock_get)
    result = get_all_stations()
    assert result == []

def test_get_current_station_air_quality():
    air_quality = get_current_station_air_quality(52)
    assert type(air_quality) == str
    assert air_quality in ("Unknown", "Bardzo dobry", "Dobry", "Umiarkowany", "Dostateczny", "Zły", "Bardzo zły")

def test_get_all_sensors_request_exception(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")
    monkeypatch.setattr(requests, "get", mock_get)
    result = get_station_sensors(55)
    assert result == []


def test_get_current_station_mesurements_api_err(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")
    monkeypatch.setattr(requests, "get", mock_get)
    result = get_current_sensor_measurements(55)
    assert result == []

def test_get_archival_station_mesurements_api_err(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.RequestException("API Error")
    monkeypatch.setattr(requests, "get", mock_get)
    result = get_archival_sensor_measurements(52, '2025-01-01 15:00', '2025-01-10 15:00')
    assert result == []

def test_get_archive_measurements_ivalid_date():
    result = get_archival_sensor_measurements(52, '12-01-2024 15:00', '2025-01-10 15:00')
    assert result == []

def test_get_archive_measurements_too_wide_range():
    result = get_archival_sensor_measurements(52, '2022-01-01 15:00', '2025-01-01 15:00')
    assert result == []

def test_get_archive_measurements_from_last_n_days_too_wide_range():
    result = get_last_n_days_sensor_measurements(52, 400)
    assert result == []

def test_get_current_station_mesurements_from_manual_sensor(capsys):
    result = get_current_sensor_measurements(276)
    captured = capsys.readouterr()
    assert 'Warning: Trying to fetch current measurements from manual-type sensor: API-ERR-100003' in captured.out
    assert result == []
