from gios_api.services import get_all_stations, get_station_sensors, get_archival_sensor_measurements, StationData, SensorData
from gios_api.models import Province, District, Commune, City, Address, Station, Sensor, Parameter, Measurement

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
        station_in_db = Station.objects.get(external_station_id=station.id)
        save_station_sensors_to_db(station_in_db, station_sensors)

def save_station_sensors_to_db(station_in_db: Station, station_sensors: list[SensorData]):
    for sensor in station_sensors:
        parameter, _ = Parameter.objects.update_or_create(
            name=sensor.indicator
        )
        Sensor.objects.update_or_create(
            external_sensor_id = sensor.id,
            defaults={
                'parameter': parameter,
                'station': station_in_db
            }
        )

def save_measurements_in_period(sensor_id: int, date_from: str, date_to: str):
    sensor_in_db = Sensor.objects.get(external_sensor_id=sensor_id)
    sensor_param = sensor_in_db.parameter
    sensor_measurements = get_archival_sensor_measurements(sensor_id, date_from, date_to)
    for mes in sensor_measurements:
        Measurement.objects.get_or_create(
            sensor=sensor_in_db,
            date=mes.date,
            defaults= {
                'value': mes.value,
                'parameter': sensor_param,
            }
        )



def update_db():
    stations = get_all_stations()
    save_stations_data_to_db(stations)
    save_sensors_data_to_db(stations)
    save_measurements_in_period(52, '2024-06-01 15:00', '2024-09-01 15:00')
