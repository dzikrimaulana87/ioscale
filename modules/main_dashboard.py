import streamlit as st
import pandas as pd
import plotly.express as px

def show_dashboard(df):
    df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"])

    st.title("📊 Dashboard Data Komoditas")

    # Layout untuk filter dalam satu baris
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pilihan_tampilan = st.selectbox("Tampilkan Berdasarkan", ["Berat (kg)", "Harga Jual (Rp)"])
    
    with col2:
        lokasi_terpilih = st.multiselect("Pilih Lokasi", df["Lokasi"].unique())

    with col3:
        komoditas_terpilih = st.multiselect("Pilih Komoditas", df["Jenis Komoditas"].unique())

    with col4:
        tanggal_awal, tanggal_akhir = st.date_input(
            "Rentang Waktu Panen",
            [df["Waktu Panen"].min(), df["Waktu Panen"].max()],
            min_value=df["Waktu Panen"].min(),
            max_value=df["Waktu Panen"].max()
        )

    # Filtering data
    filtered_df = df.copy()
    if lokasi_terpilih:
        filtered_df = filtered_df[filtered_df["Lokasi"].isin(lokasi_terpilih)]
    if komoditas_terpilih:
        filtered_df = filtered_df[filtered_df["Jenis Komoditas"].isin(komoditas_terpilih)]
    if tanggal_awal and tanggal_akhir:
        filtered_df = filtered_df[
            (filtered_df["Waktu Panen"] >= pd.to_datetime(tanggal_awal)) & 
            (filtered_df["Waktu Panen"] <= pd.to_datetime(tanggal_akhir))
        ]


    # Visualisasi dengan label X dan Y
    if not filtered_df.empty:
        if pilihan_tampilan == "Harga Jual (Rp)":
            avg_price_df = filtered_df.groupby("Jenis Komoditas")[pilihan_tampilan].mean().reset_index()
            fig = px.bar(avg_price_df, x="Jenis Komoditas", y=pilihan_tampilan, 
                         labels={"Jenis Komoditas": "Jenis Komoditas", pilihan_tampilan: "Rerata Harga Jual (Rp)"},
                         title="Rata-rata Harga Jual per Komoditas",
                         color="Jenis Komoditas")
            st.plotly_chart(fig)
        else:
            total_weight_df = filtered_df.groupby("Jenis Komoditas")[pilihan_tampilan].sum().reset_index()
            fig = px.bar(total_weight_df, x="Jenis Komoditas", y=pilihan_tampilan, 
                         labels={"Jenis Komoditas": "Jenis Komoditas", pilihan_tampilan: "Total Berat (kg)"},
                         title="Total Berat per Komoditas",
                         color="Jenis Komoditas")
            st.plotly_chart(fig)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        
# Menampilkan data hasil filtering

    st.write(f"Data berdasarkan **{pilihan_tampilan}** Komoditas")
    st.dataframe(filtered_df[["Jenis Komoditas", "Lokasi", "Waktu Panen", pilihan_tampilan]])
