import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px


def show_dashboard(df):
    df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"])

    st.title("📊 Dashboard Perbandingan Harga dan Berat Komoditas")

    # Layout filter dalam satu baris
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pilihan_tampilan = st.selectbox("Tampilkan Berdasarkan", ["Berat (kg)", "Harga Jual (Rp)"])
    
    with col2:
        lokasi_terpilih = st.multiselect("Pilih Lokasi", df["Lokasi"].unique())
    with col3:
        komoditas_pilihan = st.selectbox("Pilih Komoditas", df["Jenis Komoditas"].unique())
    with col4:
        tanggal_awal_ts, tanggal_akhir_ts = st.date_input(
            "Rentang Waktu Panen",
            [df["Waktu Panen"].min(), df["Waktu Panen"].max()],
            min_value=df["Waktu Panen"].min(),
            max_value=df["Waktu Panen"].max()
        )

    # Filtering data
    filtered_df = df.copy()
    if lokasi_terpilih:
        filtered_df = filtered_df[filtered_df["Lokasi"].isin(lokasi_terpilih)]
    filtered_df = filtered_df[filtered_df["Jenis Komoditas"] == komoditas_pilihan]
    filtered_df = filtered_df[(filtered_df["Waktu Panen"] >= pd.to_datetime(tanggal_awal_ts)) & 
                              (filtered_df["Waktu Panen"] <= pd.to_datetime(tanggal_akhir_ts))]

    # Visualisasi perbandingan antar lokasi
    if not filtered_df.empty:
        if pilihan_tampilan == "Harga Jual (Rp)":
            avg_price_df = filtered_df.groupby("Lokasi")[pilihan_tampilan].mean().reset_index()
            fig = px.bar(avg_price_df, x="Lokasi", y=pilihan_tampilan, 
                         labels={"Lokasi": "Lokasi", pilihan_tampilan: "Rata-rata Harga Jual (Rp)"},
                         title="Rata-rata Harga Jual per Lokasi",
                         color="Lokasi")
            st.plotly_chart(fig)
        else:
            total_weight_df = filtered_df.groupby("Lokasi")[pilihan_tampilan].sum().reset_index()
            fig = px.bar(total_weight_df, x="Lokasi", y=pilihan_tampilan, 
                         labels={"Lokasi": "Lokasi", pilihan_tampilan: "Total Berat (kg)"},
                         title="Total Berat per Lokasi",
                         color="Lokasi")
            st.plotly_chart(fig)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
        
    # Menampilkan data hasil filtering
    st.write(f"Data berdasarkan **{pilihan_tampilan}** Komoditas")
    st.dataframe(filtered_df[["Jenis Komoditas", "Lokasi", "Waktu Panen", pilihan_tampilan]])
