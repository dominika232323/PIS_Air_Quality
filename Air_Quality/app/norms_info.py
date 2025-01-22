import streamlit as st
import pandas as pd

concentration = {
    "Pomiar stężeń": ["Dobry", "Dostateczny", "Zły"],
    "tlenek węgla / CO [µg/m3]": ["0 - 5", "5.1 - 30", "> 30.1"],
    "benzen / SO2 [µg/m3]": ["0 - 5", "5.1 - 30", "> 30.1"],
}
concentration_df = pd.DataFrame(concentration)

quality_index = {
    "Indeks jakości powietrza": ["Bardzo dobry", "Dobry", "Umiarkowany", "Dostateczny", "Zły", "Bardzo zły"],
    "pył zawieszony PM10 [µg/m3]": ["0 - 20", "20,1 - 50", "50,1 - 80", "80,1 - 110", "110,1 - 150", "> 150"],
    "pył zawieszony PM2,5 [µg/m3]": ["0 - 13", "13,1 - 35", "35,1 - 55", "55,1 - 75", "75,1 - 110", "> 110"],
    "ozon / O3 [µg/m3]": ["0 - 70", "70,1 - 120", "120,1 - 150", "150,1 - 180", "180,1 - 240", "> 240"],
    "dwutlenek węgla / NO2 [µg/m3]": ["0 - 40", "40,1 - 100", "100,1 - 150", "150,1 - 230", "230,1 - 400", "> 400"],
    "dwutlenek siarki / SO2 [µg/m3]": ["0 - 50", "50,1 - 100", "100,1 - 200", "200,1 - 350", "350,1 - 500", "> 500"],
}
quality_index_df = pd.DataFrame(quality_index)


st.write(f"### Wybrane normy jakości powietrza")
quality_index_df_transposed = quality_index_df.transpose()
concentration_df_transposed = concentration_df.transpose()

st.write(quality_index_df_transposed)
st.write(concentration_df_transposed)
