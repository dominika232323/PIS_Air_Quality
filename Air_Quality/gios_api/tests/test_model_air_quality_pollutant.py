from datetime import datetime

import pytest

from gios_api.models import Province, District, Commune, City, Address, Station, AirQuality, AirQualityLevel, \
    AirQualityPollutant, Parameter


@pytest.fixture
def air_quality_pollutant():
    province = Province.objects.create(name="province")
    district = District.objects.create(province=province, name="district")
    commune = Commune.objects.create(district=district, name="commune")
    city = City.objects.create(commune=commune, name="city")
    address = Address.objects.create(city=city, name="address")
    station = Station.objects.create(address=address, station_name="station", external_station_id="123")

    param =  Parameter.objects.create(name="param")

    aql = AirQualityLevel.objects.create(level_name="good")

    now = datetime.now()
    aq = AirQuality.objects.create(
        station=station,
        calculate_date=now,
        air_quality_level=aql,
        source_date=now,
        index_status=True,
        critical_param="critical"
    )

    return now, AirQualityPollutant.objects.create(
        air_quality=aq,
        parameter=param,
        calculate_date=now,
        air_quality_level=aql,
        source_date=now
    )


@pytest.mark.django_db
def test_model_creation(air_quality_pollutant):
    assert air_quality_pollutant[1].parameter.name == "param"
    assert air_quality_pollutant[1].calculate_date == air_quality_pollutant[0]
    assert air_quality_pollutant[1].air_quality_level.level_name == "good"
    assert air_quality_pollutant[1].source_date == air_quality_pollutant[0]
