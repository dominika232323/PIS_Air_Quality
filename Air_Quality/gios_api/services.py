import requests
from django.http import JsonResponse

def get_all_stations():
    response = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
    return JsonResponse(response.json(), safe=False, json_dumps_params={'indent': 4})

def get_station_info(station_id: int) -> JsonResponse:
    response = requests.get(f'https://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}')
    return JsonResponse(response.json(), safe=False, json_dumps_params={'indent': 4})
