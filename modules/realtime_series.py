import streamlit as st
import pandas as pd
import plotly.express as px
from calculation.mean_calc import confidence_interval
from statsmodels.tsa.arima.model import ARIMA

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def show_realtime_series(df):

    st.title("📈 Detail Komoditas (Time Series)")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        pilihan_tampilan_time_series = st.selectbox("Tampilkan Berdasarkan", ["Berat (kg)", "Harga Jual (Rp)"])

    with col2:
        lokasi_pilihan = st.multiselect("Pilih Lokasi", df["Lokasi"].unique())

    with col3:
        komoditas_pilihan = st.selectbox("Pilih Komoditas", df["Jenis Komoditas"].unique())

    with col4:
        tanggal_awal_ts, tanggal_akhir_ts = st.date_input(
            "Rentang Waktu Panen",
            [df["Waktu Panen"].min(), df["Waktu Panen"].max()],
            min_value=df["Waktu Panen"].min(),
            max_value=df["Waktu Panen"].max()
        )
    with col5:
        pilihan_interval = st.selectbox("Pilih Interval", ["Harian", "Mingguan", "Bulanan"])

    # Filter data sesuai dengan pilihan pengguna
    filtered_df = df.copy()
    if lokasi_pilihan:
        filtered_df = filtered_df[filtered_df["Lokasi"].isin(lokasi_pilihan)]
    filtered_df = filtered_df[filtered_df["Jenis Komoditas"] == komoditas_pilihan]
    filtered_df = filtered_df[(filtered_df["Waktu Panen"] >= pd.to_datetime(tanggal_awal_ts)) & 
                              (filtered_df["Waktu Panen"] <= pd.to_datetime(tanggal_akhir_ts))]

    if filtered_df.empty:
        st.warning(f"Tidak ada data untuk {komoditas_pilihan} dalam filter yang dipilih.")
        return

    filtered_df = filtered_df.sort_values("Waktu Panen")

    # Visualisasi Time Series
    if pilihan_tampilan_time_series != "Berat (kg)":
        filtered_df[pilihan_tampilan_time_series] = pd.to_numeric(filtered_df[pilihan_tampilan_time_series], errors="coerce")
    agg_func = "sum" if pilihan_tampilan_time_series == "Berat (kg)" else "mean"
    
    if pilihan_interval == "Harian":
        df_resampled = filtered_df.groupby(filtered_df["Waktu Panen"].dt.date)[pilihan_tampilan_time_series].agg(agg_func).reset_index()
        df_resampled["Waktu Panen"] = pd.to_datetime(df_resampled["Waktu Panen"])
        judul_grafik = "📊 Data Harian"
        
    elif pilihan_interval == "Mingguan":
        df_resampled = filtered_df.set_index("Waktu Panen").resample("W")[pilihan_tampilan_time_series].agg(agg_func).reset_index()
        judul_grafik = "📆 Data Mingguan"
        
    else:  # Bulanan
        df_resampled = filtered_df.set_index("Waktu Panen").resample("M")[pilihan_tampilan_time_series].agg(agg_func).reset_index()
        judul_grafik = "📅 Data Bulanan"


    fig = px.line(df_resampled, x="Waktu Panen", y=pilihan_tampilan_time_series, markers=True, title=judul_grafik)
    st.plotly_chart(fig, use_container_width=True)
    
    #Tampilkan dugaan rentang rerata
    if pilihan_tampilan_time_series == "Harga Jual (Rp)":
        df_harga_jual = filtered_df[pilihan_tampilan_time_series].dropna()
        if not df_harga_jual.empty:
            interval_kepercayaan = confidence_interval(df_harga_jual.tolist(), confidence=0.95)
            st.subheader("📊 Rata-rata Harga Pasar")
            st.markdown(f"""
            <div style="background-color:#f0f2f6; padding: 15px; border-radius: 12px;">
                <h3 style="color:#224abe; text-align:center;">📌 Rentang Harga Jual (95% Confidence Interval)</h3>
                <p style="font-size:22px; text-align:center; color:#333;">
                    <b>{interval_kepercayaan[0]} - {interval_kepercayaan[1]} Rp</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tampilkan DataFrame
    st.subheader(f"Data **{komoditas_pilihan}** berdasarkan waktu panen:")
    st.dataframe(filtered_df[["Waktu Panen", "Lokasi", pilihan_tampilan_time_series]])
    
    if pilihan_interval == "Bulanan":
        df_monthly = df_resampled
        # Prediksi dengan ARIMA
        if len(df_monthly) > 10:
            st.subheader("🔮 Prediksi Time Series dengan ARIMA (Data Bulanan)")
            series = df_monthly.set_index("Waktu Panen")[pilihan_tampilan_time_series].astype(float)

            steps_ahead = st.slider("Pilih jumlah bulan untuk prediksi:", 1, 12, 3)

            if st.button("Jalankan Prediksi ARIMA"):
                def run_arima(series, steps):
                    try:
                        model = ARIMA(series, order=(2, 1, 2))
                        model_fit = model.fit()
                        forecast = model_fit.forecast(steps=steps)

                        if len(series) > steps:
                            actual_values = series[-steps:]
                            predicted_values = forecast[:len(actual_values)]
                            
                            mae = mean_absolute_error(actual_values, predicted_values)
                            mse = mean_squared_error(actual_values, predicted_values)
                            rmse = np.sqrt(mse)

                            return forecast, mae, mse, rmse
                        else:
                            return forecast, None, None, None
                        
                    except Exception as e:
                        return str(e), None, None, None, None

                forecast, mae, mse, rmse = run_arima(series, steps_ahead)

                if isinstance(forecast, str):
                    st.error(f"Terjadi kesalahan dalam prediksi ARIMA: {forecast}")
                else:
                    forecast_dates = pd.date_range(df_monthly["Waktu Panen"].iloc[-1], periods=steps_ahead+1, freq='M')[1:]
                    forecast_df = pd.DataFrame({pilihan_tampilan_time_series: forecast}, index=forecast_dates)

                    combined_df = pd.concat([series, forecast_df])
                    fig_forecast = px.line(combined_df, x=combined_df.index, y=pilihan_tampilan_time_series, 
                                        title="Prediksi ARIMA (2,1,2)",
                                        labels={"x": "Bulan", pilihan_tampilan_time_series: "Prediksi"},
                                        markers=True)
                    st.plotly_chart(fig_forecast, use_container_width=True)

                    st.write("Prediksi berdasarkan ARIMA:")
                    st.dataframe(forecast_df)

                    # if mae is not None:
                    #     st.subheader("📊 Evaluasi Model ARIMA")
                    #     st.write(f"- **Mean Absolute Error (MAE):** {mae:.2f}")
                    #     st.write(f"- **Mean Squared Error (MSE):** {mse:.2f}")
                    #     st.write(f"- **Root Mean Squared Error (RMSE):** {rmse:.2f}")
            else:
                st.warning("Data tidak mencukupi untuk melakukan prediksi ARIMA. Minimal 10 data bulanan.")
    else:
        st.warning("Silahkan pilih data bulanan untuk menggunakan ARIMA.")
