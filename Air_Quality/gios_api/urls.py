from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gios_api import views
from .view_sets.address_view import AddressViewSet
from .view_sets.air_quality_level_view import AirQualityLevelViewSet
from .view_sets.air_quality_pollutant_view import AirQualityPollutantViewSet
from .view_sets.air_quality_view import AirQualityViewSet
from .view_sets.city_view import CityViewSet
from .view_sets.commune_view import CommuneViewSet
from .view_sets.district_view import DistrictViewSet
from .view_sets.measurement_view import MeasurementViewSet
from .view_sets.parameter_view import ParameterViewSet
from .view_sets.province_view import ProvinceViewSet
from .view_sets.sensor_view import SensorViewSet
from .view_sets.station_view import StationViewSet


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
    path('<int:station_id>/', views.get_station_info, name='station_info'),
    path('all/', views.get_all_stations, name='all_stations'),
    path('', views.streamlit_app, name='all_stations')
]