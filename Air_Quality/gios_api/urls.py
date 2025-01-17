from django.urls import path, include
from rest_framework.routers import DefaultRouter

from views import get_station_info, get_all_stations, streamlit_app
from .views.address_view import AddressViewSet
from .views.air_quality_level_view import AirQualityLevelViewSet
from .views.air_quality_pollutant_view import AirQualityPollutantViewSet
from .views.air_quality_view import AirQualityViewSet
from .views.city_view import CityViewSet
from .views.commune_view import CommuneViewSet
from .views.district_view import DistrictViewSet
from .views.measurement_view import MeasurementViewSet
from .views.parameter_view import ParameterViewSet
from .views.province_view import ProvinceViewSet
from .views.sensor_view import SensorViewSet
from .views.station_view import StationViewSet


router = DefaultRouter()
router.register(r"address", AddressViewSet)
router.register(r"air-quality-levels", AirQualityLevelViewSet)
router.register(r"air-quality-pollutants", AirQualityPollutantViewSet)
router.register(r"air-qualities", AirQualityViewSet)
router.register(r"cities", CityViewSet)
router.register(r"communes", CommuneViewSet)
router.register(r"districts", DistrictViewSet)
router.register(r"measurements", MeasurementViewSet)
router.register(r"parameters", ParameterViewSet)
router.register(r"provinces", ProvinceViewSet)
router.register(r"sensors", SensorViewSet)
router.register(r"stations", StationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    #path('', views.welcome_user, name='welcome_page'),
    path('<int:station_id>/', get_station_info, name='station_info'),
    path('all/', get_all_stations, name='all_stations'),
    path('', streamlit_app, name='all_stations')
]