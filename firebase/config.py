import streamlit as st

FIREBASE_CONFIG = {
    "apiKey": st.secrets["firebase"]["apiKey"],
    "authDomain": st.secrets["firebase"]["authDomain"],
    "databaseURL": st.secrets["firebase"]["databaseURL"],
    "storageBucket": st.secrets["firebase"]["storageBucket"],
}
