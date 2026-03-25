from datetime import datetime
from config import Theme

class LogMixin:
    """Mixin untuk memberikan feedback visual berwarna pada aktivitas sistem."""
    def log_success(self, msg):
        # Menggunakan warna hijau dari Theme
        print(f"{Theme.OKGREEN}{Theme.ICON_SUCCESS} {msg}{Theme.ENDC}")

    def log_error(self, msg):
        # Menggunakan warna merah dan efek Tebal (Bold) untuk error
        print(f"{Theme.FAIL}{Theme.ICON_ERROR} {Theme.BOLD}{msg}{Theme.ENDC}")

    def log_warning(self, msg):
        # Menggunakan warna kuning untuk peringatan
        print(f"{Theme.WARNING}⚠️  {msg}{Theme.ENDC}")

    def log_info(self, msg):
        # Menggunakan warna biru untuk informasi sistem
        print(f"{Theme.OKBLUE}{Theme.ICON_INFO} {msg}{Theme.ENDC}")

class TimestampMixin:
    """Mixin untuk manajemen pencatatan waktu pembuatan dan pembaruan data."""
    def __init__(self):
        # Menggunakan underscore (_) untuk menjaga prinsip enkapsulasi (protected)
        self._created = datetime.now()
        self._updated = datetime.now()

    def _update_timestamp(self):
        """Memperbarui waktu modifikasi data."""
        self._updated = datetime.now()

    def get_created_at(self):
        """Mengembalikan string waktu pembuatan dengan format yang rapi."""
        return self._created.strftime("%d-%m-%Y %H:%M")

    def get_updated_at(self):
        """Mengembalikan string waktu pembaruan terakhir."""
        return self._updated.strftime("%d-%m-%Y %H:%M")