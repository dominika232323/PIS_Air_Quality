import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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

    station_measurements = st.session_state.get('sensor_results', [])
    measurements_for_sensor = station_measurements[sensor_id]
    print(f"FETCHED DATA: {measurements_for_sensor}")
    valid_measurements = [
        {"Data": m["Data"], "Wartość": m["Wartość"]}
        for m in measurements_for_sensor
        if m["Wartość"] >= 0
    ]
    sensor_df = pd.DataFrame(valid_measurements)
    try:
        sensor_df = sensor_df.sort_values(by="Data")
        st.write(f"### Wykres danych dla stacji {station_id}. {station_name} dla sensora {sensor_id}. {sensor_attribute}")
        fig = px.line(sensor_df, x="Data", y="Wartość", title=f"Wartości w czasie (od {date_from.strftime('%Y-%m-%d %H:%M')} do {date_to.strftime('%Y-%m-%d %H:%M')})",
                      labels={"Data": "Data", "Wartość": "Wartość"})
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Brak danych z wybranego okresu.")
else:
    st.warning("Nie wybrano żadnego sensora.")
