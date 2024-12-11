import requests
from gios_api.schemas import StationData, SensorData, Location, Measurement
from datetime import datetime


def map_station_json_to_object(station: dict) -> StationData:
    commune, district, voivodeship, city, street = station['Gmina'], station['Powiat'], station['Województwo'], station['Nazwa miasta'], station['Ulica']
    station_location = Location(commune, district, voivodeship, city, street)
    return StationData(station['Identyfikator stacji'], station['Nazwa stacji'], station_location)


def map_sensor_json_to_object(sensor: dict) -> SensorData:
    return SensorData(sensor['Identyfikator stanowiska'], sensor['Wskaźnik'])


def map_measurement_json_to_object(measurement: dict) -> Measurement:
    measurement_date = measurement['Data']
    measurement_date = datetime.strptime(measurement_date, "%Y-%m-%d %H:%M:%S")
    return Measurement(measurement_date, float(measurement['Wartość']))


def convert_json_into_sensors_objects(sensors: list[dict]) -> list[SensorData]:
    sensors_data = []
    for sensor in sensors:
        sensor_data = map_sensor_json_to_object(sensor)
        sensors_data.append(sensor_data)
    return sensors_data


def convert_json_into_stations_objects(stations: list[dict]) -> list[StationData]:
    stations_data = []
    for station in stations:
        station_data = map_station_json_to_object(station)
        stations_data.append(station_data)
    return stations_data


def convert_json_into_measurements_objects(measurements: list[dict]) -> list[Measurement]:
    measurements_data = []
    for measurement in measurements:
        mes_data = map_measurement_json_to_object(measurement)
        measurements_data.append(mes_data)
    return measurements_data


def get_all_stations() -> list[StationData]:
    params = {'sort': 'id'}
    response = requests.get('https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll', params=params).json()
    stations = response['Lista stacji pomiarowych']
    return convert_json_into_stations_objects(stations)


def get_station_sensors(station_id: int) -> list[SensorData]:
    response = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}').json()
    sensors = response['Lista stanowisk pomiarowych dla podanej stacji']
    return convert_json_into_sensors_objects(sensors)


def get_current_sensor_measurements(sensor_id: int) -> list[Measurement]:
    params = {'sort': 'Data'}
    response = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{sensor_id}', params=params).json()
    measurements = response['Lista danych pomiarowych']
    return convert_json_into_measurements_objects(measurements)
