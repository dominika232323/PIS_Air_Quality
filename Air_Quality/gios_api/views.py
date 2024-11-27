from django.shortcuts import render, HttpResponse
from . import services

def welcome_user(request):
    return HttpResponse("Welcome! To see all stations, use /all. To see specific station info use /station_id")

def get_all_stations(request):
    return services.get_all_stations()

def get_station_info(request, station_id: int):
    return services.get_station_info(station_id)
