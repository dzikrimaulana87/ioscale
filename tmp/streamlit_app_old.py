import streamlit as st
import pandas as pd
from calculation.mean_calc import confidence_interval

# Data dan preproses awal
data = {
    "Jenis Komoditas": [
        "Padi", "Jagung", "Kedelai", "Padi", "Jagung", "Kopi", "Tebu", "Kentang", "Padi", "Kedelai",
        "Jagung", "Kopi", "Tebu", "Kentang", "Kedelai", "Padi", "Jagung", "Kopi", "Tebu", "Kentang",
        "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung", "Jagung"
    ],
    "Berat (kg)": [
        500, 700, 400, 600, 800, 1200, 1500, 900, 650, 450,
        750, 1300, 1600, 1000, 500, 550, 850, 1400, 1550, 1100,
        720, 810, 920, 870, 930, 950, 970, 1020, 1080, 1150
    ],
    "Harga Jual (Rp)": [
        5000000, 7000000, 4000000, 6000000, 8000000, 15000000, 17000000, 9000000, 6500000, 4500000,
        7500000, 13000000, 17500000, 11000000, 5000000, 5500000, 8500000, 14000000, 16500000, 12000000,
        7200000, 8100000, 9200000, 8700000, 9300000, 9500000, 9700000, 10200000, 10800000, 11500000
    ],
    "Lokasi": [
        "Bandung", "Jakarta", "Surabaya", "Bandung", "Jakarta", "Medan", "Semarang", "Malang", "Bali", "Yogyakarta",
        "Jakarta", "Aceh", "Surabaya", "Lombok", "Bandung", "Semarang", "Bogor", "Makassar", "Palembang", "Padang",
        "Lampung", "Solo", "Pontianak", "Manado", "Balikpapan", "Jambi", "Palangkaraya", "Kupang", "Batam", "Ambon"
    ],
    "Waktu Panen": [
        "2024-01", "2024-02", "2024-01", "2024-03", "2024-02", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08",
        "2024-02", "2024-05", "2024-03", "2024-07", "2024-01", "2024-06", "2024-09", "2024-10", "2024-11", "2024-12",
        "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11"
    ]
}
df = pd.DataFrame(data)
df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"])

# ===== Tampilan Dashboard Utama =====
st.title("📊 Dashboard Data Komoditas")
pilihan_tampilan = st.selectbox("Tampilkan Data Berdasarkan:", ["Berat (kg)", "Harga Jual (Rp)"])
lokasi_terpilih = st.multiselect("Pilih Lokasi:", df["Lokasi"].unique())

st.subheader("Pilih Rentang Waktu Panen:")
tanggal_awal, tanggal_akhir = st.date_input(
    "Rentang Waktu Panen",
    [df["Waktu Panen"].min(), df["Waktu Panen"].max()],
    min_value=df["Waktu Panen"].min(),
    max_value=df["Waktu Panen"].max()
)

komoditas_terpilih = st.multiselect("Pilih Jenis Komoditas:", df["Jenis Komoditas"].unique())

filtered_df = df.copy()
if lokasi_terpilih:
    filtered_df = filtered_df.loc[filtered_df["Lokasi"].isin(lokasi_terpilih)]
if komoditas_terpilih:
    filtered_df = filtered_df.loc[filtered_df["Jenis Komoditas"].isin(komoditas_terpilih)]
if tanggal_awal and tanggal_akhir:
    filtered_df = filtered_df[
        (filtered_df["Waktu Panen"] >= pd.to_datetime(tanggal_awal)) & 
        (filtered_df["Waktu Panen"] <= pd.to_datetime(tanggal_akhir))
    ]

st.write(f"Menampilkan data berdasarkan **{pilihan_tampilan}**:")
st.dataframe(filtered_df[["Jenis Komoditas", "Lokasi", "Waktu Panen", pilihan_tampilan]])

if not filtered_df.empty:
    if pilihan_tampilan == "Harga Jual (Rp)":
        avg_price_df = filtered_df.groupby("Jenis Komoditas")[pilihan_tampilan].mean()
        st.bar_chart(avg_price_df)
    else:
        total_weight_df = filtered_df.groupby("Jenis Komoditas")[pilihan_tampilan].sum()
        st.bar_chart(total_weight_df)
else:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# ===== Detail Time Series =====
st.title("📈 Detail Komoditas")
pilihan_tampilan_time_series = st.radio("Tampilkan Data Berdasarkan (Time Series):", ["Berat (kg)", "Harga Jual (Rp)"])
komoditas_pilihan = st.selectbox("Pilih satu jenis komoditas:", df["Jenis Komoditas"].unique())
lokasi_pilihan_time_series = st.multiselect("Pilih Lokasi (Time Series):", df["Lokasi"].unique())

st.subheader("Pilih Rentang Waktu Panen (Time Series):")
tanggal_awal_ts, tanggal_akhir_ts = st.date_input(
    "Rentang Waktu Panen (Time Series)",
    [df["Waktu Panen"].min(), df["Waktu Panen"].max()],
    min_value=df["Waktu Panen"].min(),
    max_value=df["Waktu Panen"].max()
)


df_komoditas = df[df["Jenis Komoditas"] == komoditas_pilihan].copy()
if lokasi_pilihan_time_series:
    df_komoditas = df_komoditas[df_komoditas["Lokasi"].isin(lokasi_pilihan_time_series)]
if tanggal_awal_ts and tanggal_akhir_ts:
    df_komoditas = df_komoditas[
        (df_komoditas["Waktu Panen"] >= pd.to_datetime(tanggal_awal_ts)) & 
        (df_komoditas["Waktu Panen"] <= pd.to_datetime(tanggal_akhir_ts))
    ]
df_komoditas = df_komoditas.sort_values("Waktu Panen")

if pilihan_tampilan_time_series == "Harga Jual (Rp)":
    df_harga_jual = df_komoditas[["Waktu Panen", "Lokasi", pilihan_tampilan_time_series]]
    harga_jual_list = df_harga_jual[pilihan_tampilan_time_series].to_list()
    interval_kepercayaan = confidence_interval(harga_jual_list, confidence=0.95)

    st.write(interval_kepercayaan)

st.write(f"Data **{komoditas_pilihan}** berdasarkan waktu panen:")
st.dataframe(df_komoditas[["Waktu Panen", "Lokasi", pilihan_tampilan_time_series]])



if not df_komoditas.empty:
    st.line_chart(df_komoditas.set_index("Waktu Panen")[pilihan_tampilan_time_series])
    
    st.subheader("🔮 Prediksi Time Series dengan ARIMA")
    if len(df_komoditas) > 10:
        df_komoditas["Waktu Panen"] = pd.to_datetime(df_komoditas["Waktu Panen"])
        df_komoditas.set_index("Waktu Panen", inplace=True)
        series = df_komoditas[pilihan_tampilan_time_series].astype(float)
        
        steps_ahead = st.slider("Pilih jumlah hari untuk prediksi:", 1, 30, 7)
        
        if st.button("Jalankan Prediksi ARIMA"):
            # Import ARIMA hanya saat dibutuhkan
            from statsmodels.tsa.arima.model import ARIMA

            # Fungsi untuk menjalankan ARIMA dengan caching agar tidak perlu memodel ulang
            @st.experimental_memo(show_spinner=False)
            def run_arima(series_tuple, steps):
                # Konversi kembali tuple ke Series
                series = pd.Series(series_tuple, index=series.index)
                model = ARIMA(series, order=(2, 1, 2))
                model_fit = model.fit()
                return model_fit.forecast(steps=steps)

            # Karena Series tidak hashable, konversi ke tuple sebagai kunci cache
            series_tuple = tuple(series)
            forecast = run_arima(series_tuple, steps_ahead)

            # Buat DataFrame prediksi
            forecast_dates = pd.date_range(series.index[-1], periods=steps_ahead+1, freq='D')[1:]
            forecast_df = pd.DataFrame({pilihan_tampilan_time_series: forecast}, index=forecast_dates)
            combined_df = pd.concat([series, forecast_df])
            
            st.line_chart(combined_df)
            st.write("Prediksi berdasarkan ARIMA (2,1,2):")
            st.dataframe(forecast_df)
    else:
        st.warning("Data terlalu sedikit untuk prediksi ARIMA. Gunakan rentang waktu lebih panjang.")
else:
    st.warning(f"Tidak ada data untuk {komoditas_pilihan} dalam filter yang dipilih.")
