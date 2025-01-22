import streamlit as st
import pandas as pd
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

thresholds = {
    "pył zawieszony PM10": [(0, 20), (20.1, 50), (50.1, 80), (80.1, 110), (110.1, 150), (150.1, float('inf'))],
    "pył zawieszony PM2.5": [(0, 13), (13.1, 35), (35.1, 55), (55.1, 75), (75.1, 110), (110.1, float('inf'))],
    "ozon": [(0, 70), (70.1, 120), (120.1, 150), (150.1, 180), (180.1, 240), (240.1, float('inf'))],
    "dwutlenek azotu": [(0, 40), (40.1, 100), (100.1, 150), (150.1, 230), (230.1, 400), (400.1, float('inf'))],
    "dwutlenek siarki": [(0, 50), (50.1, 100), (100.1, 200), (200.1, 350), (350.1, 500), (500.1, float('inf'))],
	"tlenek węgla": [(-5, -0.9), (0, 5), (-30, -5.1), (5.1, 30), (30.1, float('inf')), (-float('inf'), -30.1)],
	"benzen": [(-5, -0.9), (0, 5), (-30, -5.1), (5.1, 30), (30.1, float('inf')), (-float('inf'), -30.1)],
}

labels = ["Bardzo dobry", "Dobry", "Umiarkowany", "Dostateczny", "Zły", "Bardzo zły"]
def assign_pollution_level(value, indicator):
    if indicator in thresholds:
        for i, (low, high) in enumerate(thresholds[indicator]):
            if low <= value <= high:
                return labels[i]
    return "Nieuwzględniony"

station_data = fetch_measurements_with_station_data()
stations_df = pd.DataFrame(station_data)

stations_df.insert(1, "Poziom zanieczyszczeń", stations_df.apply(lambda row: assign_pollution_level(row["Wartość"], row["Wskaźnik"]), axis=1))

st.write("### Ostrzeżenia z ostatniej godziny")

column1, column2, column3 = st.columns(3)
with column1:
    indicator_query = st.text_input("Wyszukaj po wskaźniku")
with column2:
    pollution_level_filter = st.selectbox(
        "Filtruj po poziomie zanieczyszczeń",
        options=["", "Bardzo zły", "Zły", "Dostateczny", "Umiarkowany", "Dobry", "Bardzo dobry"]
	)
with column3:
    location_query = st.text_input("Wyszukaj po lokalizacji:")

filtered_df = stations_df.copy()
if indicator_query:
    filtered_df = filtered_df[filtered_df['Wskaźnik'].str.contains(indicator_query, case=False, na=False)]
if location_query:
    filtered_df = filtered_df[
        filtered_df.apply(
            lambda row: row.astype(str).str.contains(location_query, case=False, na=False).any(), axis=1
        )
    ]
if pollution_level_filter:
    filtered_df = filtered_df[filtered_df['Poziom zanieczyszczeń'] == pollution_level_filter]

gb = GridOptionsBuilder.from_dataframe(filtered_df)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_selection("single")
for col in filtered_df.columns:
    gb.configure_column(col, autoWidth=True)


gb.configure_columns(["ID Stacji", "Nazwa Stacji", "ID Sensora"], hide=True)

grid_options = gb.build()

grid_response = AgGrid(
	filtered_df,
	gridOptions=grid_options,
)

selected_row = pd.DataFrame(grid_response.get("selected_rows", []))
if not selected_row.empty:
	selected_measurement = selected_row.iloc[0]
	st.session_state.selected_station_id = selected_measurement["ID Stacji"]
	st.session_state.selected_station_name = selected_measurement["Nazwa Stacji"]
	st.session_state.selected_sensor_id = selected_measurement["ID Sensora"]
	st.session_state.selected_sensor_attribute = selected_measurement["Wskaźnik"]
	st.switch_page("current/plot.py")
