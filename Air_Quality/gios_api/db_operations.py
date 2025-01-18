from gios_api.services import get_all_stations, StationData
from gios_api.models import Province

def save_provinces_to_db(stations: list[StationData]):
    for station_data in stations:
        Province.objects.update_or_create(
            name=station_data.location.voivodeship
        )


def update_db():
    print("Updating Database...")
    stations = get_all_stations()
    save_provinces_to_db(stations)
    print("Done")
