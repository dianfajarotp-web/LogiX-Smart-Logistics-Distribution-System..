from mixins import LogMixin, TimestampMixin
from config import Theme

class Toko(LogMixin, TimestampMixin):
    def __init__(self, id_toko, nama):
        super().__init__()
        # Enkapsulasi atribut private
        self._id = id_toko
        self._nama = nama
        self._stok = {} # {barang_id: jumlah}

        self.log_success(f"[{self.get_created_at()}] {Theme.ICON_STORE} Cabang Toko '{Theme.BOLD}{self._nama}{Theme.ENDC}' telah terdaftar.")

    # --- GETTER ---
    @property
    def id(self): return self._id

    @property
    def nama(self): return self._nama

    # --- LOGIC TOKO ---
    def terima_barang(self, barang_id, jumlah):
        """Menerima kiriman barang dari gudang pusat."""
        if jumlah <= 0:
            self.log_error("Jumlah penerimaan barang harus positif!")
            raise ValueError("Jumlah harus > 0")

        self._stok[barang_id] = self._stok.get(barang_id, 0) + jumlah
        self._update_timestamp()
        self.log_info(f"[{self.get_updated_at()}] {Theme.ICON_BOX} {self._nama} menerima stok: ID {barang_id} (+{jumlah})")


    def cek_stok(self):
        """Melihat inventaris toko saat ini."""
        return self._stok

    def to_dict(self):
        """Konversi data untuk JSON."""
        return {
            "id": self._id,
            "nama": self._nama,
            "stok": self._stok,
            "updated_at": self.get_updated_at()
        }