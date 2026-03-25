from datetime import datetime
from mixins import LogMixin
from config import Theme

class Distribusi(LogMixin):
    """
    Kelas untuk mengelola alur distribusi barang.
    Mencatat pergerakan barang dari Gudang ke Toko beserta riwayat statusnya.
    """
    def __init__(self, barang, toko, jumlah, gudang, history=None):
        self.barang = barang
        self.toko = toko
        self.jumlah = jumlah
        self.gudang = gudang

        if history is not None:
            # ✅ pakai history lama (dari database)
            self.history = history
        else:
            # ✅ hanya buat baru kalau distribusi baru
            self.history = []
            self.tambah_history("📦 DIKIRIM")

    def tambah_history(self, status):
        """Menambahkan catatan waktu pada riwayat distribusi."""
        waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.history.append({
            "status": status,
            "waktu": waktu_sekarang
        })

    def update_status(self, status):
        """Memperbarui status pengiriman dengan validasi."""
        status_valid = ["dikirim", "sampai", "proses", "tertunda"]
        if status.lower() not in status_valid:
            self.log_error(f"Status '{status}' tidak valid!")
            raise ValueError("Status tidak valid")
        
        icon = "🚚" if status.lower() == "dikirim" else "✅"
        self.tambah_history(f"{icon} {status.upper()}")
        self.log_info(f"Update Logistik: Barang {self.barang} status kini {status.upper()}")


    def tampilkan_detail(self):
        """Menampilkan kartu informasi distribusi yang rapi."""
        print(f"\n{Theme.OKCYAN}{'='*40}{Theme.ENDC}")
        print(f"{Theme.BOLD}   DETAIL PENGIRIMAN LOGISTIK{Theme.ENDC}")
        print(f"{Theme.OKCYAN}{'='*40}{Theme.ENDC}")
        print(f" {Theme.ICON_BOX}  Produk  : {Theme.BOLD}{self.barang}{Theme.ENDC}")
        print(f" {Theme.ICON_STORE} Cabang  : {self.toko}")
        print(f" 🏭  Asal    : {self.gudang}")
        print(f" 🔢  Jumlah  : {self.jumlah} unit")
        print(f"{Theme.OKCYAN}{'-'*40}{Theme.ENDC}")
        print(f"{Theme.BOLD} Riwayat Perjalanan:{Theme.ENDC}")
        for h in self.history:
            print(f"  • {h['status']} ({h['waktu']})")
        print(f"{Theme.OKCYAN}{'='*40}{Theme.ENDC}\n")

    def to_dict(self):
        """Konversi ke dictionary untuk penyimpanan JSON."""
        return {
            "barang": self.barang,
            "toko": self.toko,
            "jumlah": self.jumlah,
            "gudang": self.gudang,
            "history": self.history
        }

    @staticmethod
    def from_dict(data):
        return Distribusi(
        data.get("barang", "Unknown"),
        data.get("toko", "Unknown"),
        data.get("jumlah", 0),
        data.get("gudang", "-"),
        history=data.get("history", [])
    )