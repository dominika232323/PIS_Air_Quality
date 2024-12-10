import requests
from django.http import JsonResponse
from gios_api.schemas import StationData, Location

def map_station_json_to_object(station: dict) -> StationData:
    commune, district, voivodeship, city, street = station['Gmina'], station['Powiat'], station['Województwo'], station['Nazwa miasta'], station['Ulica']
    station_location = Location(commune, district, voivodeship, city, street)
    return StationData(station['Identyfikator stacji'], station['Nazwa stacji'], station_location)

def convert_json_into_stations_objects(stations: list[dict]) -> list[StationData]:
    stations_data = []
    for station in stations:
        station_data = map_station_json_to_object(station)
        stations_data.append(station_data)
    return stations_data

def get_all_stations() -> list[StationData]:
    params = {'sort': 'id'}
    response = requests.get('https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll', params=params).json()
    stations = response['Lista stacji pomiarowych']
    return convert_json_into_stations_objects(stations)

def get_station_info(station_id: int) -> JsonResponse:
    response = requests.get(f'https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}')
    return JsonResponse(response.json(), safe=False, json_dumps_params={'indent': 4})
