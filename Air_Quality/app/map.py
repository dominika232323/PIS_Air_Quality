import folium
import streamlit as st
from streamlit_folium import folium_static
import pandas as pd

import requests

url = "https://api.gios.gov.pl/pjp-api/rest/station/findAll"
response = requests.get(url)

if response.status_code == 200:
    stations = response.json()
else:
    stations = []

station_data = [
    {
        "id": station["id"],
        "stationName": station["stationName"],
        "latitude": float(station["gegrLat"]),
        "longitude": float(station["gegrLon"]),
        "city": station["city"]["name"],
        "addressStreet": station["addressStreet"]
    }
    for station in stations
]

stations_df = pd.DataFrame(station_data)

map_center = [stations_df["latitude"].mean(), stations_df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=6)

for _, row in stations_df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"{row['city']}<br>{row['addressStreet']}",
    ).add_to(m)

st.write("### Mapa Stacji")
st_data = folium_static(m)