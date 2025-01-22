from gios_api.models import Sensor, Measurement
from datetime import datetime, timedelta
from gios_api.services import get_archival_sensor_measurements
from gios_api.db_operations import save_measurements_in_period

def check_db_for_measurements_in_period(sensor_id: str, date_from: str, date_to: str):
    date_from_dt = datetime.strptime(date_from, '%Y-%m-%d %H:%M')
    date_to_dt = datetime.strptime(date_to, '%Y-%m-%d %H:%M')
    sensor_in_db = Sensor.objects.filter(external_sensor_id=sensor_id).first()
    if sensor_in_db is None or date_from_dt.date() > date_to_dt.date():
        return []
    measurements = Measurement.objects.filter(sensor=sensor_in_db, date__gte = date_from_dt, date__lte = date_to_dt).order_by("date")
    if len(measurements) < (date_to_dt - date_from_dt).days:
        print(f"Saving data for {sensor_id} from: {date_from} to: {date_to}")
        save_measurements_in_period(sensor_id, date_from, date_to)
        measurements = Measurement.objects.filter(sensor=sensor_in_db, date__gte = date_from_dt, date__lte = date_to_dt).order_by("date")
    return measurements
