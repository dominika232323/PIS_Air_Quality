from gios_api.services import get_all_stations, get_station_sensors, StationData, SensorData
from gios_api.models import Province, District, Commune, City, Address, Station, Sensor, Parameter

def save_stations_data_to_db(stations: list[StationData]):
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

        if station_data.location.street:
            address, _ = Address.objects.update_or_create(
                name=station_data.location.street,
                city=city
            )
        else:
            address, _ = Address.objects.update_or_create(
                name=f"Station {station_data.name}",
                city=city
            )

        station, _ = Station.objects.update_or_create(
            external_station_id=station_data.id,
            defaults={
                'station_name': station_data.name,
                'address': address
                }
        )



def save_sensors_data_to_db(stations: list[StationData]):
    for station in stations:
        station_sensors = get_station_sensors(station.id)
        station_in_db = Station.objects.get(station_name=station.name)
        save_station_sensors_to_db(station_in_db, station_sensors)

def save_station_sensors_to_db(station_in_db: Station, station_sensors: list[SensorData]):
    for sensor in station_sensors:
        parameter, _ = Parameter.objects.update_or_create(
            name=sensor.indicator
        )
        Sensor.objects.update_or_create(
            external_sensor_id = sensor.id,
            defaults={'parameter': parameter,
                      'station': station_in_db
                    }
        )



def update_db():
    stations = get_all_stations()
    save_stations_data_to_db(stations)
    save_sensors_data_to_db(stations)
