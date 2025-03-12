import collections
import collections.abc
collections.MutableMapping = collections.abc.MutableMapping
import time
import pyrebase
from firebase.config import FIREBASE_CONFIG

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
    return _cached_data