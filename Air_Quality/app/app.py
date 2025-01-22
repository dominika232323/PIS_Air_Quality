import streamlit as st

welcome_page = st.Page("welcomepage.py", title="Strona powitalna", icon="👋")
norms_info_page = st.Page("norms_info.py", title="Normy jakości powietrza", icon="💨")
map_page = st.Page("map.py", title="Mapa stacji", icon="🌍")
stations_page = st.Page("stations.py", title="Stacje", icon="🗼")
alert_page = st.Page("current/alerts.py", title="Ostrzeżenia", icon="🚨")
sensor_data_page = st.Page("current/sensor_data.py", title="Dane z sensorów", icon="📡")
plot_page = st.Page("current/plot.py", title="Wykres najnowszych pomiarów", icon="📈")
past_sensor_data_page = st.Page("past/past_sensor_data.py", title="Archiwalne dane z sensorów", icon="📡")
past_plot_page = st.Page("past/past_plot.py", title="Wykres archiwalnych pomiarów", icon="📈")
agregated_page = st.Page("agregated/agregated.py", title="Histogramy średnich wartości", icon="📊")

if 'selected_station_id' not in st.session_state:
    st.session_state.selected_station_id = None
if 'selected_station_name' not in st.session_state:
    st.session_state.selected_station_name = None
if 'selected_sensor_id' not in st.session_state:
    st.session_state.selected_station_id = None
if 'selected_station_attribute' not in st.session_state:
    st.session_state.selected_station_attribute = None
    
pg = st.navigation({"Ogólne": [welcome_page, norms_info_page, map_page, stations_page], "Aktualne dane": [alert_page, sensor_data_page, plot_page], "Dane archiwalne": [past_sensor_data_page, past_plot_page], "Zagregowane informacje": [agregated_page]})
pg.run()