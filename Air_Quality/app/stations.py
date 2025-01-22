import streamlit as st
import pandas as pd
import requests
from st_aggrid import AgGrid, GridOptionsBuilder
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gios_api.services import get_all_stations

stations = requests.get("http://127.0.0.1:8000/stations/").json()

stations_data = [
    {
        "ID": station.get("external_station_id"),
        "Ulica": station.get("address", {}).get("name", "Brak danych"),
        "Miasto": station.get("address", {}).get("city", {}).get("name", "Brak danych"),
        "Województwo": station.get("address", {}).get("city", {}).get("commune", {}).get("district", {}).get("province", {}).get("name", "Brak danych"),
        "Powiat": station.get("address", {}).get("city", {}).get("commune", {}).get("district", {}).get("name", "Brak danych"),
        "Gmina": station.get("address", {}).get("city", {}).get("commune", {}).get("name", "Brak danych"),
        "Nazwa Stacji": station.get("station_name", "Brak danych"),
    }
    for station in stations
]
stations_df = pd.DataFrame(stations_data)

st.write("### Wszystkie stacje")
search_query = st.text_input("Wyszukaj w stacjach:")
filtered_df = stations_df.copy()
if search_query:
    filtered_df = filtered_df[
        filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(), axis=1)
    ]

gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection("single")
for col in filtered_df.columns:
    gb.configure_column(col, autoWidth=True)


gb.configure_columns(["ID", "Nazwa Stacji"], hide=True)

grid_options = gb.build()
grid_response = AgGrid(
    filtered_df,
	gridOptions=grid_options,
)

selected_row = pd.DataFrame(grid_response.get("selected_rows", []))
if not selected_row.empty:
    selected_station = selected_row.iloc[0]
    st.session_state.selected_station_id = selected_station["ID"]
    st.session_state.selected_station_name = selected_station["Nazwa Stacji"]
    st.switch_page("current/sensor_data.py")