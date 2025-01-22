import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from gios_api.services import get_archival_sensor_measurements, get_last_n_days_sensor_measurements

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
def fetch_sensor_measurements(sensor_id, date_from, date_to):
    return get_archival_sensor_measurements(sensor_id, date_from, date_to)

@st.cache_data
def fetch_last_n_days_sensor_measurements(sensor_id, n_days):
    return get_last_n_days_sensor_measurements(sensor_id, n_days)

station_id = st.session_state.get("selected_station_id")
station_name = st.session_state.get("selected_station_name")
sensor_id = st.session_state.get("selected_sensor_id")
sensor_attribute = st.session_state.get("selected_sensor_attribute")
if sensor_id:
    left, middle, right = st.columns(3)
    date_from = datetime.today() - timedelta(weeks=1)
    date_to = datetime.today()
    if left.button("Ostatni tydzień", use_container_width=True):
        date_from = datetime.today() - timedelta(weeks=1)
        date_to = datetime.today()
    if middle.button("Ostatni miesiąc", use_container_width=True):
        date_from = datetime.today() - relativedelta(months=1)
        date_to = datetime.today()
    if right.button("Ostatni rok", use_container_width=True):
        date_from = datetime.today() - relativedelta(years=1)
        date_to = datetime.today()

    sensor_measurements = fetch_sensor_measurements(sensor_id, date_from.strftime('%Y-%m-%d %H:%M'), date_to.strftime('%Y-%m-%d %H:%M'))
    valid_measurements = [
        {"Data": m.date, "Wartość": m.value}
        for m in sensor_measurements
        if m.value >= 0
    ]
    sensor_df = pd.DataFrame(valid_measurements)

    try:
        sensor_df = sensor_df.sort_values(by="Data")
        st.write(f"### Wykres danych dla stacji {station_id}. {station_name} dla sensora {sensor_id}. {sensor_attribute}")
        fig = px.line(sensor_df, x="Data", y="Wartość", title=f"Wartości w czasie (od {date_from.strftime('%Y-%m-%d %H:%M')} do {date_to.strftime('%Y-%m-%d %H:%M')})",
                      labels={"Data": "Data", "Wartość": "Wartość"})
        limits = quality_index.get(sensor_attribute, [])
        colors = ["green", "lightgreen", "yellow", "orange", "red", "darkred"]
        labels = ["Bardzo dobry", "Dobry", "Umiarkowany", "Dostateczny", "Zły", "Bardzo zły"]
        for idx, limit in enumerate(limits):
            fig.add_hline(y=limit, line_dash="dash", line_color=colors[idx], annotation_text=f"{labels[idx]} (Limit {limit})",
                          annotation_position="top right")
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Brak danych z wybranego okresu.")
else:
    st.warning("Nie wybrano żadnego sensora.")
