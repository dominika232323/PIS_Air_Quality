from gios_api.services import get_all_stations, StationData
from gios_api.models import Province, District, Commune, City, Address, Station

def save_station_data_to_db(stations: list[StationData]):
    for station_data in stations:
        province, _ = Province.objects.update_or_create(
            name=station_data.location.voivodeship
        )

        district, _ = District.objects.update_or_create(
            name=station_data.location.district,
            defaults= {'province': province}
        )

        commune, _ = Commune.objects.update_or_create(
            name=station_data.location.commune,
            defaults={'district': district}
        )

        city, _ = City.objects.update_or_create(
            name=station_data.location.city,
            defaults={'commune': commune}
        )

        address, _ = Address.objects.update_or_create(
            name=station_data.location.street or 'Unknown Street',
            defaults={'city': city}
        )


        station, _ = Station.objects.update_or_create(
            station_name=station_data.name,
            defaults={'address': address}
        )



def update_db():
    stations = get_all_stations()
    save_station_data_to_db(stations)
