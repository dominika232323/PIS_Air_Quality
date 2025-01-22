import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from gios_api.services import get_current_sensor_measurements

quality_index = {
    "pył zawieszony PM10": [20, 50, 80, 110, 150],
    "pył zawieszony PM2.5": [13, 35, 55, 75, 110],
    "ozon": [70, 120, 150, 180, 240],
    "dwutlenek węgla": [40, 100, 150, 230, 400],
    "dwutlenek siarki": [50, 100, 200, 350, 500],
    "tlenek węgla": [5, 30],
    "benzen": [5, 30]
}

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
    limits = quality_index.get(sensor_attribute, [])
    colors = ["green", "lightgreen", "yellow", "orange", "red", "darkred"]
    labels = ["Bardzo dobry", "Dobry", "Umiarkowany", "Dostateczny", "Zły", "Bardzo zły"]
    for idx, limit in enumerate(limits):
        fig.add_hline(y=limit, line_dash="dash", line_color=colors[idx], annotation_text=f"{labels[idx]} (Limit {limit})",
                      annotation_position="top right")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Nie wybrano żadnego sensora.")
