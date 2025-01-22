import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from gios_api.services import get_all_stations, get_station_sensors, get_current_sensor_measurements

@st.cache_data
def fetch_measurements_with_station_data():
    stations = get_all_stations()
    station_data = []

    for station in stations:
        station_sensors = get_station_sensors(station.id)
        for sensor in station_sensors:
            measurements = get_current_sensor_measurements(sensor.id)
            if measurements:
                measurement = measurements[0]
                if measurement:
                    if measurement.value != -1:
                        station_data.append({
                            "Wskaźnik": sensor.indicator,
                            "Wartość": measurement.value,
                            "Data": measurement.date,
                            "Miasto": station.location.city,
                            "Ulica": station.location.street or "Brak danych",
                            "Gmina": station.location.commune,
                            "Powiat": station.location.district,
                            "Województwo": station.location.voivodeship,
                            "ID Stacji": station.id,
                            "Nazwa Stacji": station.name,
                            "ID Sensora": sensor.id,
                        })

    return station_data

data = fetch_measurements_with_station_data()
df = pd.DataFrame(data)

def plot_histogram(group_by_column):
    grouped_df = df.groupby(group_by_column)['Wartość'].mean().reset_index()
    fig = px.bar(grouped_df, x=group_by_column, y='Wartość')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
    
st.markdown("### Średnia dla województw")
plot_histogram('Województwo')

st.markdown("### Średnia dla powiatów")
plot_histogram('Powiat')

st.markdown("### Średnia dla gmin")
plot_histogram('Gmina')
