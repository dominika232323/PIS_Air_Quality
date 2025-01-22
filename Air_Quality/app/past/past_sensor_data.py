import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from gios_api.services import get_station_sensors, get_last_n_days_sensor_measurements

@st.cache_data
def fetch_station_sensors(station_id):
    return get_station_sensors(station_id)

@st.cache_data
def fetch_sensor_measurements(sensor_id, last_n_days):
    return get_last_n_days_sensor_measurements(sensor_id, last_n_days)

station_id = st.session_state.selected_station_id
station_name = st.session_state.selected_station_name

if not station_id:
    st.warning("Nie wybrano żadnej stacji.")
else:
    last_n_days = st.slider(
        "Wybierz sprzed ilu dni chcesz pobrać dane:",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
    )
    sensors = fetch_station_sensors(station_id)
    sensor_results = []
    for sensor in sensors:
        sensor_data = fetch_sensor_measurements(sensor.id, last_n_days)
        if sensor_data:
            min_measurement = min(sensor_data, key=lambda x: x.value if x.value is not None else float('inf'))
            max_measurement = max(sensor_data, key=lambda x: x.value if x.value is not None else float('-inf'))
            latest_measurement = sensor_data[0]
            if latest_measurement:
                sensor_results.append({
                "Sensor": sensor.indicator,
                "ID Sensora": sensor.id,
                "Data": latest_measurement.date,
                "Wartość": latest_measurement.value,
                "Min Wartość": min_measurement.value,
                "Data Min": min_measurement.date,
                "Max Wartość": max_measurement.value,
                "Data Max": max_measurement.date
                })

    results_df = pd.DataFrame(sensor_results)
    st.write(f"### Dane sprzed {last_n_days} dni dla sensorów na stacji {station_id}. {station_name}")
    gb_sensors = GridOptionsBuilder.from_dataframe(results_df)
    gb_sensors.configure_selection("single")
    gb_sensors.configure_auto_height(autoHeight=True)

    gb_sensors.configure_columns(["ID Sensora"], hide=True)

    grid_options_sensors = gb_sensors.build()
    grid_response_sensors = AgGrid(
        results_df,
        gridOptions=grid_options_sensors,
        fit_columns_on_grid_load=True,
    )
    selected_sensor_row = pd.DataFrame(grid_response_sensors.get("selected_rows", []))
    if not selected_sensor_row.empty:
        selected_sensor = selected_sensor_row.iloc[0]
        st.session_state.selected_sensor_id = selected_sensor["ID Sensora"]
        st.session_state.selected_sensor_attribute = selected_sensor["Sensor"]
        st.switch_page("current/plot.py")