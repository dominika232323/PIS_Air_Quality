from gios_api.models import Sensor, Measurement
from datetime import datetime, timedelta

def check_db_for_measurements_in_period(sensor_id: str, date_from: str, date_to: str):
    # naive iterate and check
    # better? - get set where id ==id and date between () len == from-finish
    print(Sensor.objects.all())
    date_from = datetime.strptime(date_from, '%Y-%m-%d %H:%M')
    date_to = datetime.strptime(date_to, '%Y-%m-%d %H:%M')
    try:
        if date_from.date() > date_to.date():
            return "no"
        sensor_in_db = Sensor.objects.get(external_sensor_id=sensor_id)
        measurements = Measurement.objects.filter(sensor=sensor_in_db, date__gte = date_from, date__lte = date_to).order_by("date").distinct('date')
        if len(measurements) < (date_to - date_from).days:
            # identify missing measurements
            return
        print(measurements)
        return measurements
    except Exception as e:
        print(e)
        return "exc"