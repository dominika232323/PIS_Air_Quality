import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import sys
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Air_Quality.settings')
django.setup()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from datetime import datetime, timedelta
import requests
from gios_api.db_services import check_db_for_measurements_in_period

@st.cache_data
def fetch_station_sensors(station_id):
    return requests.get(f'http://127.0.0.1:8000/sensors/station/{station_id}').json()

def fetch_sensor_measurements(sensor_id, last_n_days):
    current_date = datetime.now()
    date_n_days_before = current_date - timedelta(days=last_n_days)
    print(f"Fetching sensor date from: {date_n_days_before} to: {current_date}")
    return check_db_for_measurements_in_period(sensor_id, date_n_days_before.strftime('%Y-%m-%d %H:%M'), current_date.strftime('%Y-%m-%d %H:%M'))

station_id = st.session_state.get("selected_station_id")
station_name = st.session_state.get("selected_station_name")

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
    if st.button("Pobierz dane"):
        st.session_state["sensor_results"] = {}

        for sensor in sensors:
            sensor_id = sensor['external_sensor_id']
            sensor_mes = fetch_sensor_measurements(sensor_id, last_n_days)

            if sensor_mes:
                st.session_state["sensor_results"][sensor_id] = [
                    {"Data": mes.date, "Wartość": mes.value} for mes in sensor_mes
                ]

    if "sensor_results" in st.session_state and st.session_state["sensor_results"]:
        sensors_summary = []

        for sensor in sensors:
            sensor_id = sensor['external_sensor_id']
            sensor_data = st.session_state["sensor_results"].get(sensor_id, [])
            print(f"Sensor DATA: {sensor_data}")

            num_measurements = len(sensor_data)

            sensors_summary.append({
                "Sensor": sensor["parameter"]["name"],
                "ID Sensora": sensor_id,
                "Liczba pomiarów": num_measurements,
            })

        summary_df = pd.DataFrame(sensors_summary)
        st.write(f"### Podsumowanie danych dla sensorów sprzed {last_n_days} dni (Stacja: {station_name})")

        gb_sensors = GridOptionsBuilder.from_dataframe(summary_df)
        gb_sensors.configure_selection("single")
        gb_sensors.configure_auto_height(autoHeight=True)

        grid_options_sensors = gb_sensors.build()
        grid_response_sensors = AgGrid(
            summary_df,
            gridOptions=grid_options_sensors,
            fit_columns_on_grid_load=True,
        )

        selected_sensor_row = pd.DataFrame(grid_response_sensors.get("selected_rows", []))
        if not selected_sensor_row.empty:
            selected_sensor = selected_sensor_row.iloc[0]
            st.session_state.selected_sensor_id = selected_sensor["ID Sensora"]
            st.session_state.selected_sensor_attribute = selected_sensor["Sensor"]
            st.switch_page("past/past_plot.py")