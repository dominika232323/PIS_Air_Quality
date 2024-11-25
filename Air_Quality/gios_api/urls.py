from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_user, name='welcome_page'),
    path('<int:station_id>/', views.get_station_info, name='station_info'),
    path('all/', views.get_all_stations, name='all_stations')
]