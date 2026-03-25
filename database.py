import json
import os
from config import Config, Theme

class Database:

    # ✅ FIX: Satu sumber data default
    DEFAULT_DATA = {
        "barang": {},
        "supplier": {},
        "gudang": {},
        "toko": {},
        "distribusi": [],
        "users": {
            "fajar": {"password": "123", "role": "supervisor", "nama": "fajar"},
        }
    }

    def __init__(self):
        # Memastikan file database ada saat inisialisasi
        if not os.path.exists(Config.DB_FILE):
            self.data = self.DEFAULT_DATA.copy()
            self.save()
        else:
            self.load()

    def load(self):
        """Memuat data dari file JSON dengan penanganan error jika file rusak."""
        try:
            with open(Config.DB_FILE, "r") as f:
                self.data = json.load(f)

            # ✅ FIX: Pastikan struktur minimal tetap ada
            for key in self.DEFAULT_DATA:
                if key not in self.data:
                    self.data[key] = self.DEFAULT_DATA[key]

            # ✅ FIX: Pastikan user default tidak hilang
            if not self.data.get("users"):
                print(f"{Theme.WARNING}⚠️ Data user kosong, memulihkan default user...{Theme.ENDC}")
                self.data["users"] = self.DEFAULT_DATA["users"]

        except (json.JSONDecodeError, IOError) as e:
            print(f"{Theme.FAIL}{Theme.ICON_ERROR} Gagal memuat database: {e}{Theme.ENDC}")

            # ✅ FIX: Gunakan default lengkap (bukan kosong)
            self.data = self.DEFAULT_DATA.copy()

            # ✅ FIX: Auto-repair file
            self.save()
            print(f"{Theme.OKGREEN}✅ Database diperbaiki otomatis dengan data default.{Theme.ENDC}")

    def save(self):
        """Menyimpan data ke file JSON."""
        try:
            with open(Config.DB_FILE, "w") as f:
                json.dump(self.data, f, indent=4)
        except IOError as e:
            print(f"{Theme.FAIL}{Theme.ICON_ERROR} Gagal menyimpan data: {e}{Theme.ENDC}")

    def refresh(self):
        self.load()