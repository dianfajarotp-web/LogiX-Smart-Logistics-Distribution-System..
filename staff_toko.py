from user import User
from config import Theme

class StaffToko(User):
    """
    Kelas untuk peran Staff Toko/Cabang.
    Fokus pada penjualan barang ke konsumen dan pemantauan stok di cabang.
    """
    def __init__(self, username, password, nama):
        # Memanggil constructor parent (User)
        super().__init__(username, password, nama)

    def akses_menu(self):
        """
        Implementasi method abstrak akses_menu.
        Memberikan hak akses untuk operasional retail.
        """
        return [
            "cek stok toko",
            "tambah toko", # Sesuai syntax asli Anda
            "keluar"
        ]

    def tampilkan_welcome(self):
        """Pesan selamat datang khusus staff toko dengan warna identitas."""
        print(f"\n{Theme.OKGREEN}{Theme.BOLD}--- PANEL OPERASIONAL CABANG TOKO ---{Theme.ENDC}")
        self.tampilkan_profil()
        print(f"{Theme.OKGREEN}Status: Store Access (Sales & Retail){Theme.ENDC}\n")