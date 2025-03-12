import streamlit as st
from firebase import data_loader
from modules import main_dashboard
from modules import realtime_series
from modules import daerah_dashboard

st.set_page_config(page_title="Dashboard Komoditas", page_icon="📊", layout="wide")

custom_css = """
<style>
/* Styling Sidebar */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #4e73df 0%, #224abe 100%);
    color: white;
    padding: 1rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: white;
}

[data-testid="stSidebar"] .css-1aumxhk {
    background: transparent;
}

[data-testid="stSidebar"] .stRadio > div {
    margin-bottom: 1rem;
}

/* Styling judul halaman utama */
h1 {
    color: #224abe;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

df = data_loader.get_data_from_firebase()

# Sidebar Navigasi
st.sidebar.title("Menu Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", ("Dashboard Utama", "Data Time Series", "Data Daerah"))

# Panggil halaman sesuai pilihan
if halaman == "Dashboard Utama":
    main_dashboard.show_dashboard(df)

elif halaman == "Data Time Series":
    realtime_series.show_realtime_series(df)

elif halaman == "Data Daerah":
    daerah_dashboard.show_dashboard(df)
