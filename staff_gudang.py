from user import User
from config import Theme

class StaffGudang(User):
    """
    Kelas untuk peran Staff Gudang.
    Fokus pada manajemen fisik barang dan penyimpanan di gudang.
    """
    def __init__(self, username, password, nama):
        # Memanggil constructor parent (User)
        super().__init__(username, password, nama)

    def akses_menu(self):
        """
        Implementasi method abstrak akses_menu.
        Memberikan hak akses terbatas pada fungsi inventaris gudang.
        """
        return [
            "tambah barang", 
            "manajemen stok", 
            "tambah gudang",
            "cek stok gudang",
            "keluar"
        ]

    def tampilkan_welcome(self):
        """Pesan selamat datang khusus staff gudang dengan warna identitas."""
        print(f"\n{Theme.OKBLUE}{Theme.BOLD}--- PANEL OPERASIONAL GUDANG ---{Theme.ENDC}")
        self.tampilkan_profil()
        print(f"{Theme.OKBLUE}Status: Gudang Access (Inventory Only){Theme.ENDC}\n")