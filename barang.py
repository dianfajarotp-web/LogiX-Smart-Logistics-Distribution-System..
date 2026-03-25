from mixins import LogMixin, TimestampMixin
from config import Theme

class Barang(LogMixin, TimestampMixin):
    def __init__(self, id_barang, nama, harga, stok=0):
        # Inisialisasi dari TimestampMixin
        super().__init__()

        # --- VALIDASI PROFESIONAL ---
        if not str(nama).strip():
            self.log_error("Gagal membuat barang: Nama tidak boleh kosong!")
            raise ValueError("Nama tidak boleh kosong")

        if int(harga) <= 0:
            self.log_error(f"Gagal membuat barang '{nama}': Harga harus lebih dari 0!")
            raise ValueError("Harga harus > 0")

        if int(stok) < 0:
            self.log_error(f"Gagal membuat barang '{nama}': Stok tidak boleh negatif!")
            raise ValueError("Stok tidak boleh negatif")

        # --- ENKAPSULASI ---
        self._id = id_barang
        self._nama = nama.strip()
        self._harga = int(harga)
        self._stok = int(stok)

        self.log_success(
            f"[{self.get_created_at()}] {Theme.ICON_BOX} Barang '{Theme.BOLD}{self._nama}{Theme.ENDC}' berhasil didaftarkan."
        )

    # --- GETTER ---
    @property
    def id(self):
        return self._id

    @property
    def nama(self):
        return self._nama

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, value):
        """Setter tambahan agar konsisten dengan property"""
        if value < 0:
            self.log_error(f"Update stok '{self._nama}' gagal: Stok tidak boleh negatif!")
            raise ValueError("Stok tidak boleh negatif")
        
        self._stok = value
        self._update_timestamp()
        self.log_info(f"[{self.get_updated_at()}] {Theme.ICON_INFO} Stok diset langsung: {self._nama} = {value}")

    @property
    def harga(self):
        return self._harga

    @property
    def harga_fmt(self):
        """Mengembalikan harga dalam format mata uang."""
        return f"Rp {self._harga:,}".replace(",", ".")

    # --- METHOD LAMA (TETAP DIPERTAHANKAN) ---
    def set_stok(self, stok: int):
        if stok < 0:
            self.log_error(f"Update stok '{self._nama}' gagal: Stok tidak boleh negatif!")
            raise ValueError("Stok tidak boleh negatif")

        self._stok = stok
        self._update_timestamp()
        self.log_info(f"[{self.get_updated_at()}] {Theme.ICON_INFO} Stok diperbarui: {self._nama} = {stok}")

    def tambah_stok(self, jumlah: int):
        if jumlah <= 0:
            self.log_error(f"Input gagal: Jumlah tambah stok '{self._nama}' harus positif!")
            raise ValueError("Jumlah harus > 0")

        self._stok += jumlah
        self._update_timestamp()
        self.log_success(
            f"[{self.get_updated_at()}] {Theme.ICON_SUCCESS} Stok {self._nama} bertambah +{jumlah} (Total: {self._stok})"
        )

    def kurangi_stok(self, jumlah: int):
        if jumlah > self._stok:
            self.log_error(f"Transaksi gagal: Stok '{self._nama}' tidak mencukupi! (Sisa: {self._stok})")
            raise ValueError("Stok tidak cukup")

        if jumlah <= 0:
            self.log_error("Jumlah pengurangan harus lebih dari 0")
            raise ValueError("Jumlah harus > 0")

        self._stok -= jumlah
        self._update_timestamp()
        self.log_warning(
            f"[{self.get_updated_at()}] {Theme.ICON_TRUCK} Stok {self._nama} dikurangi -{jumlah} (Sisa: {self._stok})"
        )

    def to_dict(self):
        """Konversi objek ke dictionary untuk disimpan di JSON."""
        return {
            "id": self._id,
            "nama": self._nama,
            "harga": self._harga,
            "stok": self._stok,
            "created_at": self.get_created_at(),
            "updated_at": self.get_updated_at()
        }