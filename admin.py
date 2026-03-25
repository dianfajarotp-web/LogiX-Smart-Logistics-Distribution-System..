from user import User
from config import Theme

class Supervisor(User):
    """
    Kelas untuk peran Administrator/Supervisor.
    Memiliki hak akses penuh terhadap seluruh fitur sistem LogiX.
    """

    def __init__(self, username, password, nama):
        # Memanggil constructor parent (User) untuk menyimpan kredensial
        super().__init__(username, password, nama)

    def akses_menu(self):
        """
        Implementasi method abstrak dari class User.
        Mengembalikan daftar menu yang diizinkan untuk Supervisor.
        """
        return [
            "tambah user",          # ✅ FIX: ditambahkan agar sinkron dengan main.py
            "tambah barang",
            "manajemen stok",
            "tambah gudang", 
            "tambah toko", 
            "distribusi barang",
            "update status distribusi", 
            "laporan lengkap",
            "keluar"
        ]

    def tampilkan_welcome(self):
        """Pesan selamat datang khusus admin dengan warna identitas."""
        print(f"\n{Theme.HEADER}{Theme.BOLD}--- PANEL KONTROL SUPERVISOR ---{Theme.ENDC}")
        self.tampilkan_profil()
        print(f"{Theme.OKCYAN}Status: Superuser (Full Access){Theme.ENDC}\n")