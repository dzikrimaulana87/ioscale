import streamlit as st
import pandas as pd
from firebase.data_loader2 import get_data_from_firebase

st.title("Dashboard Data Komoditas (Realtime dengan Listener & Cache)")

cached_data = get_data_from_firebase()

if cached_data:
    try:
        df = pd.DataFrame.from_dict(cached_data, orient="index")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Gagal memproses data: {e}")
else:
    st.warning("Menunggu data dari Firebase...")
