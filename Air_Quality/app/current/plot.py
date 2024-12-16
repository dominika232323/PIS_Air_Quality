import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from gios_api.services import get_current_sensor_measurements

@st.cache_data
def fetch_sensor_measurements(sensor_id):
    return get_current_sensor_measurements(sensor_id)

station_id = st.session_state.get("selected_station_id")
station_name = st.session_state.get("selected_station_name")
sensor_id = st.session_state.get("selected_sensor_id")
sensor_attribute = st.session_state.get("selected_sensor_attribute")
if sensor_id:
    sensor_measurements = fetch_sensor_measurements(sensor_id)
    valid_measurements = [
        {"Data": m.date, "Wartość": m.value}
        for m in sensor_measurements
        if m.value >= 0
    ]
    sensor_df = pd.DataFrame(valid_measurements)
    sensor_df = sensor_df.sort_values(by="Data")

    st.write(f"### Wykres danych dla stacji {station_id}. {station_name} dla sensora {sensor_id}. {sensor_attribute}")
    fig = px.line(sensor_df, x="Data", y="Wartość", title="Wartości w czasie",
                          labels={"Data": "Data", "Wartość": "Wartość"})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nie wybrano żadnego sensora.")
