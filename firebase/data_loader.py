import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
import time
import pyrebase
from firebase.config import FIREBASE_CONFIG

## Load dummy data
import pandas as pd

def load_dummy():
    df = pd.read_csv("firebase/dummy.csv")
    df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"])
    return df
## End of Load dummy data

# Inisialisasi Firebase
firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
db = firebase.database()

# Variabel untuk caching
_CACHE_TTL = 180  # Time-to-live: 3 menit dalam detik
_last_fetch_time = 0
_cached_data = None

def get_data_from_firebase():
    """
    Mengembalikan data dari Firebase.
    Data hanya diambil ulang jika sudah lebih dari 3 menit sejak pengambilan terakhir,
    sehingga jika user refresh terus menerus, data yang di-cache akan digunakan.
    """
    global _last_fetch_time, _cached_data
    current_time = time.time()
    if (current_time - _last_fetch_time) > _CACHE_TTL or _cached_data is None:
        # Jika cache sudah kadaluarsa atau belum ada data, ambil data baru dari Firebase.
        _cached_data = db.child("data").get().val()
        _last_fetch_time = current_time
    df = pd.DataFrame.from_dict(_cached_data, orient='index')
    df = df.T.T.reset_index(drop=True)
    df = df.rename(columns={
        "komoditas": "Jenis Komoditas",
        "total_berat": "Berat (kg)",
        "total_harga": "Harga Jual (Rp)",
        "kota": "Lokasi",
        "waktu": "Waktu Panen"
    })
    df["Berat (kg)"] = pd.to_numeric(df["Berat (kg)"], errors="coerce")
    df["Harga Jual (Rp)"] = pd.to_numeric(df["Harga Jual (Rp)"], errors="coerce")
    df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"], errors='coerce')
    
    df = df.dropna()
    df = df[["Jenis Komoditas", "Berat (kg)", "Harga Jual (Rp)", "Lokasi", "Waktu Panen"]]
    df["Waktu Panen"] = df["Waktu Panen"].dt.normalize()
    dummy = load_dummy()
    df = pd.concat([df,dummy])
    df["Waktu Panen"] = pd.to_datetime(df["Waktu Panen"], errors='coerce')
    return df
