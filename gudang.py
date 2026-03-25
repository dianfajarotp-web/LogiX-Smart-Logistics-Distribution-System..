from mixins import LogMixin, TimestampMixin
from config import Theme

class Gudang(LogMixin, TimestampMixin):
    def __init__(self, id_gudang, nama):
        super().__init__()
        # Enkapsulasi: Menggunakan (_) untuk atribut internal
        self._id = id_gudang
        self._nama = nama
        self._stok = {} # Dictionary: {barang_id: jumlah}

        self.log_success(f"[{self.get_created_at()}] {Theme.ICON_STORE} Gudang '{Theme.BOLD}{self._nama}{Theme.ENDC}' berhasil diinisialisasi.")

    # --- GETTER ---
    @property
    def id(self):
        return self._id

    @property
    def nama(self):
        return self._nama

    # --- LOGIC GUDANG ---
    def tambah_barang(self, barang_id, jumlah):
        """Menambah stok barang ke gudang dengan validasi."""
        if jumlah <= 0:
            self.log_error(f"Gudang {self._nama}: Jumlah tambah harus lebih dari 0!")
            raise ValueError("Jumlah harus > 0")

        self._stok[barang_id] = self._stok.get(barang_id, 0) + jumlah
        self._update_timestamp()
        self.log_info(f"[{self.get_updated_at()}] {Theme.ICON_BOX} Masuk ke {self._nama}: ID {barang_id} (+{jumlah})")

    def kurangi_barang(self, barang_id, jumlah):
        """Mengurangi stok untuk distribusi dengan pengecekan ketersediaan."""
        if jumlah <= 0:
            self.log_error("Jumlah pengurangan harus lebih dari 0")
            raise ValueError("Jumlah harus > 0")

        if barang_id not in self._stok or self._stok[barang_id] < jumlah:
            stok_ada = self._stok.get(barang_id, 0)
            self.log_error(f"Gudang {self._nama}: Stok ID {barang_id} tidak cukup! (Tersedia: {stok_ada})")
            raise ValueError("Stok tidak cukup di gudang")

        self._stok[barang_id] -= jumlah
        self._update_timestamp()
        self.log_warning(f"[{self.get_updated_at()}] {Theme.ICON_TRUCK} Keluar dari {self._nama}: ID {barang_id} (-{jumlah})")

    def cek_stok(self):
        """Mengembalikan dictionary stok saat ini."""
        return self._stok

    def to_dict(self):
        """Konversi untuk penyimpanan database JSON."""
        return {
            "id": self._id,
            "nama": self._nama,
            "stok": self._stok,
            "updated_at": self.get_updated_at()
        }