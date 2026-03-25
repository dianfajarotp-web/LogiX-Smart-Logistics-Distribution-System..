import os

class Theme:
    # --- ANSI Color Codes ---
    HEADER    = '\033[95m' # Magenta Muda
    OKBLUE    = '\033[94m' # Biru
    OKCYAN    = '\033[96m' # Cyan
    OKGREEN   = '\033[92m' # Hijau
    WARNING   = '\033[93m' # Kuning
    FAIL      = '\033[91m' # Merah
    ENDC      = '\033[0m'  # Reset Warna
    BOLD      = '\033[1m'  # Tebal
    UNDERLINE = '\033[4m'  # Garis Bawah

    # --- Emojis & Symbols ---
    ICON_SUCCESS = "✅"
    ICON_ERROR   = "❌"
    ICON_INFO    = "ℹ️ "
    ICON_BOX     = "📦"
    ICON_TRUCK   = "🚚"
    ICON_STORE   = "🏪"
    ICON_USER    = "👤"
    LOCK         = "🔒"

class Config:
    DB_FILE = "db.json"
    APP_NAME = "LogiX - Smart Logistics Distribution System"
    VERSION = "v2.0 (Enhanced Edition)"
    
    @staticmethod
    def display_splash():
        """Menampilkan judul dan deskripsi aplikasi saat startup"""
        # Membersihkan layar terminal (cls untuk windows, clear untuk mac/linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        width = 70
        print(f"{Theme.OKCYAN}{'='*width}{Theme.ENDC}")
        print(f"{Theme.BOLD}{Theme.HEADER}{Config.APP_NAME.center(width)}{Theme.ENDC}")
        print(f"{Theme.OKCYAN}{Config.VERSION.center(width)}{Theme.ENDC}")
        print(f"{Theme.OKCYAN}{'='*width}{Theme.ENDC}")
        
        print(f"\n{Theme.BOLD}DESKRIPSI SISTEM:{Theme.ENDC}")
        print(f"LogiX adalah solusi manajemen rantai pasok digital yang dirancang untuk")
        print(f"mengotomatisasi distribusi barang dari Gudang Pusat ke berbagai")
        print(f"cabang Toko secara real-time dan terintegrasi.")
        
        print(f"\n{Theme.BOLD}FITUR UTAMA:{Theme.ENDC}")
        print(f" {Theme.ICON_BOX} Manajemen Inventaris & Multi-Gudang")
        print(f" {Theme.ICON_TRUCK} Distribusi Stok Otomatis")
        print(f" {Theme.ICON_STORE} Monitoring Stok Cabang")
        print(f" {Theme.ICON_SUCCESS} Pelaporan Laba & Arus Barang")
        
        print(f"\n{Theme.OKCYAN}{'-'*width}{Theme.ENDC}")
        input(f" {Theme.ICON_INFO} Tekan {Theme.BOLD}[ENTER]{Theme.ENDC} untuk melanjutkan ke sistem login...")