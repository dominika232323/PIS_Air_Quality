from django.shortcuts import render, HttpResponse
from . import services

def gios(request):
    return services.get_station_info(515)
