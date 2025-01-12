import requests
from gios_api.schemas import StationData, SensorData, Location, Measurement
from datetime import datetime
from gios_api.errors import InvalidDateFormatError, TooWideDateRangeError

def map_station_json_to_object(station: dict) -> StationData:
    location = station['city']['commune']
    station_location = Location(
        location['communeName'],
        location['districtName'],
        location['provinceName'],
        station['city']['name'],
        station['addressStreet']
    )
    return StationData(station['id'], station['stationName'], station_location)


def map_sensor_json_to_object(sensor: dict) -> SensorData:
    return SensorData(sensor['Identyfikator stanowiska'], sensor['Wskaźnik'])


def map_measurement_json_to_object(measurement: dict) -> Measurement:
    try:
        measurement_date = measurement['Data']
        measurement_date = datetime.strptime(measurement_date, "%Y-%m-%d %H:%M:%S")
        value = float(measurement['Wartość'])
        if value < 0:
            raise ValueError("Value cannot be negative")
        return Measurement(measurement_date, value)
    except (ValueError, TypeError, KeyError) as err:
        print(f"Warning Ivalid Data: {err}")
        return Measurement(None, -1)


def convert_json_into_sensors_objects(sensors: list[dict]) -> list[SensorData]:
    sensors_data = [map_sensor_json_to_object(sensor) for sensor in sensors]
    return sensors_data


def convert_json_into_stations_objects(stations: list[dict]) -> list[StationData]:
    stations_data = [map_station_json_to_object(station) for station in stations]
    return stations_data


def convert_json_into_measurements_objects(measurements: list[dict]) -> list[Measurement]:
    measurements_data = [map_measurement_json_to_object(measurement) for measurement in measurements]
    return measurements_data

def check_date_format(date: str, valid_format: str='%Y-%m-%d %H:%M'):
    try:
        datetime.strptime(date, valid_format)
    except ValueError:
        raise InvalidDateFormatError(f'Invalid Date format! Expected Format: {valid_format}. Got: {date}')

def get_days_between_two_dates(first_date: datetime, second_date: datetime) -> int:
    diff = abs(first_date - second_date)
    return diff.days

def check_date_wide(start_date: str, end_date: str, date_format: str='%Y-%m-%d %H:%M'):
    start, end = datetime.strptime(start_date, date_format), datetime.strptime(end_date, date_format)
    MAX_DIFF = 366
    if get_days_between_two_dates(start, end) > 366:
        raise TooWideDateRangeError(f'Too Wide Range between Dates! Max diff is: {MAX_DIFF}')

def fetch_data_from_api(url: str, params: dict[str, str]= {}) -> dict:
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()

def validate_dates(date_from: str, date_to: str):
    check_date_format(date_from)
    check_date_format(date_to)
    check_date_wide(date_from, date_to)

def get_all_stations() -> list[StationData]:
    try:
        stations = fetch_data_from_api('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
        return convert_json_into_stations_objects(stations)
    except requests.RequestException as e:
        print(f"An error occured while trying to fetch stations data: {e}")
        return []


def get_station_sensors(station_id: int) -> list[SensorData]:
    try:
        response = fetch_data_from_api(f'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}')
        sensors = response['Lista stanowisk pomiarowych dla podanej stacji']
        return convert_json_into_sensors_objects(sensors)
    except requests.RequestException as e:
        print(f"An error occured while trying to fetch sensors: {e}")
        return []


def get_current_sensor_measurements(sensor_id: int) -> list[Measurement]:
    try:
        response = fetch_data_from_api(f'https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}')
        measurements = response['Lista danych pomiarowych']
        return convert_json_into_measurements_objects(measurements)
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 400:
            error_details = http_err.response.json()
            error_code = error_details["error_code"]
            if error_code == "API-ERR-100003":
                print(f"Warning: Trying to fetch current measurements from manual-type sensor: {error_code}")
        return []
    except requests.RequestException as e:
        print(f"An error occured while trying to fetch sensor's measurements: {e}")
        return []


def get_archival_sensor_measurements(sensor_id: int, date_from: str, date_to: str) -> list[Measurement]:
    try:
        validate_dates(date_from, date_to)
        params = {"dateFrom": date_from, "dateTo": date_to}
        response = fetch_data_from_api(f'https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataBySensor/{sensor_id}', params)
        measurements = response['Lista archiwalnych wyników pomiarów']
        return convert_json_into_measurements_objects(measurements)
    except InvalidDateFormatError:
        return []
    except TooWideDateRangeError:
        return []
    except requests.RequestException as e:
        print(f"An error occured while trying to fetch sensor's archival measurements: {e}")
        return []

def get_last_n_days_sensor_measurements(sensor_id: int, n_days: int) -> list[Measurement]:
    try:
        params = {"dayNumber": n_days}
        response = fetch_data_from_api(f'https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataBySensor/{sensor_id}', params)
        measurements = response['Lista archiwalnych wyników pomiarów']
        return convert_json_into_measurements_objects(measurements)
    except requests.RequestException as e:
        print(f"An error occured while trying to fetch sensor's archival measurements: {e}")
        return []
