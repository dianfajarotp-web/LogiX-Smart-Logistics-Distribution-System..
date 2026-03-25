import os
from config import Config, Theme
from database import Database
from auth import Auth
from barang import Barang
from gudang import Gudang
from admin import Supervisor
from staff_gudang import StaffGudang
from staff_toko import StaffToko
from toko import Toko
from distribusi import Distribusi
from laporan import Laporan

# Inisialisasi Database Global
db = Database()

# ================= VALIDASI INPUT =================

def input_angka(prompt):
    while True:
        try:
            return int(input(f"{Theme.ICON_INFO} {prompt}"))
        except ValueError:
            print(f"{Theme.FAIL}❌ Harus berupa angka!{Theme.ENDC}")

def input_tidak_kosong(prompt):
    while True:
        data = input(f"{Theme.ICON_INFO} {prompt}").strip()
        if data:
            return data
        print(f"{Theme.FAIL}❌ Input tidak boleh kosong!{Theme.ENDC}")

# ================= FUNGSI OPERASIONAL =================

def tambah_user():
    print(f"\n{Theme.OKCYAN}--- FORM TAMBAH USER BARU ---{Theme.ENDC}")
    username = input_tidak_kosong("Username Baru: ").lower().strip()
    
    if username in db.data.get("users", {}):
        print(f"{Theme.FAIL}❌ Username sudah terdaftar!{Theme.ENDC}")
        return

    password = input_tidak_kosong("Password: ")
    nama = input_tidak_kosong("Nama Lengkap: ")
    
    print(f"\nPilih Role:")
    print("1. Supervisor")
    print("2. Staff Gudang")
    print("3. Staff Toko")

    # 🔥 VALIDASI INPUT
    while True:
        pilihan = input("Pilih (1/2/3): ").strip()
        if pilihan in ["1", "2", "3"]:
            break
        print("❌ Pilihan hanya boleh 1, 2, atau 3!")

    role_map = {
        "1": "supervisor",
        "2": "staff_gudang",
        "3": "staff_toko"
    }

    role = role_map[pilihan]

    db.data["users"][username] = {
        "password": password,
        "role": role,
        "nama": nama
    }

    db.save()
    print(f"{Theme.OKGREEN}✅ User {nama} berhasil didaftarkan!{Theme.ENDC}")
    input("\nTekan Enter...")

def tambah_barang():
    print(f"\n{Theme.OKCYAN}--- FORM TAMBAH BARANG BARU ---{Theme.ENDC}")
    id_b = input_tidak_kosong("ID Barang: ")

    if id_b in db.data["barang"]:
        print(f"{Theme.FAIL}❌ ID sudah digunakan!{Theme.ENDC}")
        return

    nama = input_tidak_kosong("Nama Barang: ")
    harga = input_angka("Harga Satuan: ")

    id_g = input_tidak_kosong("Masukkan ID Gudang Penempatan: ")

    if id_g not in db.data["gudang"]:
        print(f"{Theme.FAIL}❌ Gudang tidak ditemukan!{Theme.ENDC}")
        return

    jumlah = input_angka("Jumlah Stok Awal: ")

    if jumlah <= 0 or harga <= 0:
        print(f"{Theme.FAIL}❌ Input tidak valid!{Theme.ENDC}")
        return

    barang = Barang(id_b, nama, harga)
    db.data["barang"][id_b] = barang.to_dict()

    gudang_data = db.data["gudang"][id_g]
    gudang_data["stok"][id_b] = gudang_data["stok"].get(id_b, 0) + jumlah

    db.save()
    print(f"{Theme.OKGREEN}✅ Barang berhasil didaftarkan ke Gudang {id_g}!{Theme.ENDC}")
    input("\nTekan Enter...")

def tambah_gudang():
    print(f"\n{Theme.OKCYAN}--- REGISTRASI GUDANG BARU ---{Theme.ENDC}")
    id_g = input_tidak_kosong("ID Gudang: ")

    if id_g in db.data["gudang"]:
        print(f"{Theme.FAIL}❌ ID Gudang sudah ada!{Theme.ENDC}")
        return
        
    nama = input_tidak_kosong("Nama Lokasi Gudang: ")
    db.data["gudang"][id_g] = {"nama": nama, "stok": {}}

    db.save()
    print(f"{Theme.OKGREEN}✅ Gudang berhasil ditambahkan!{Theme.ENDC}")
    input("\nTekan Enter...")

def tambah_toko():
    print(f"\n{Theme.OKCYAN}--- TAMBAH TOKO ---{Theme.ENDC}")
    id_t = input_tidak_kosong("ID Toko: ")

    if id_t in db.data["toko"]:
        print(f"{Theme.FAIL}❌ ID sudah ada!{Theme.ENDC}")
        return

    nama = input_tidak_kosong("Nama Toko: ")
    db.data["toko"][id_t] = {"nama": nama, "stok": {}}

    db.save()
    print(f"{Theme.OKGREEN}✅ Toko berhasil ditambahkan!{Theme.ENDC}")
    input("\nEnter...")
    
def manajemen_stok():
    print(f"\n{Theme.OKCYAN}--- MANAJEMEN STOK ---{Theme.ENDC}")
    print("1. Tambah stok")
    print("2. Kurangi stok")
    print("0. Kembali")

    # 🔥 VALIDASI MENU
    while True:
        pilih = input("Pilih (1/2/0): ").strip()
        if pilih in ["1", "2", "0"]:
            break
        print("❌ Pilihan hanya boleh 1, 2, atau 0!")

    # 🔥 JIKA PILIH 0 → LANGSUNG KELUAR
    if pilih == "0":
        return

    id_g = input_tidak_kosong("ID Gudang: ")
    id_b = input_tidak_kosong("ID Barang: ")
    jumlah = input_angka("Jumlah: ")

    try:
        # 🔥 VALIDASI GUDANG
        if id_g not in db.data["gudang"]:
            print("❌ Gudang tidak ditemukan!")
            return

        gudang_data = db.data["gudang"][id_g]
        gudang_obj = Gudang(id_g, gudang_data["nama"])
        gudang_obj._stok = gudang_data["stok"]

        if pilih == "1":
            # tambah stok
            if jumlah <= 0:
                print("❌ Jumlah harus lebih dari 0!")
                return

            gudang_obj.tambah_barang(id_b, jumlah)

        elif pilih == "2":
            # 🔥 VALIDASI BARANG
            if id_b not in gudang_obj._stok:
                print("❌ Barang tidak ada di gudang!")
                return

            # 🔥 VALIDASI STOK
            if jumlah > gudang_obj._stok[id_b]:
                print(f"❌ Stok tidak cukup! Sisa: {gudang_obj._stok[id_b]}")
                return

            gudang_obj.kurangi_barang(id_b, jumlah)

        db.data["gudang"][id_g]["stok"] = gudang_obj._stok
        db.save()

        print("✅ Berhasil update stok!")

    except Exception as e:
        print(f"{Theme.FAIL}❌ {e}{Theme.ENDC}")

    input("\nEnter...")

def distribusi():
    print(f"\n{Theme.OKCYAN}--- PROSES KIRIM BARANG ---{Theme.ENDC}")

    id_g = input_tidak_kosong("ID Gudang: ")
    id_b = input_tidak_kosong("ID Barang: ")
    id_t = input_tidak_kosong("ID Toko: ")
    jumlah = input_angka("Jumlah: ")

    try:
        # ================= VALIDASI =================

        # 1. Gudang harus ada
        if id_g not in db.data["gudang"]:
            print("❌ Gudang tidak ditemukan!")
            input("Enter...")
            return

        # 2. Toko harus ada
        if id_t not in db.data["toko"]:
            print("❌ Toko tidak ditemukan!")
            input("Enter...")
            return

        stok_gudang = db.data["gudang"][id_g]["stok"]

        # 3. Barang harus ada di gudang
        if id_b not in stok_gudang:
            print("❌ Barang tidak ada di gudang!")
            input("Enter...")
            return

        stok_tersedia = stok_gudang[id_b]

        # 4. Jumlah tidak boleh <= 0
        if jumlah <= 0:
            print("❌ Jumlah harus lebih dari 0!")
            input("Enter...")
            return

        # 🔥 5. VALIDASI PENTING (INI YANG KAMU MAU)
        if jumlah > stok_tersedia:
            print(f"❌ Stok tidak cukup!")
            print(f"👉 Stok tersedia: {stok_tersedia}")
            input("Enter...")
            return

        # ================= PROSES =================

        toko_data = db.data["toko"][id_t]
        toko_obj = Toko(id_t, toko_data["nama"])
        toko_obj._stok = toko_data["stok"]

        # kurangi stok gudang
        stok_gudang[id_b] -= jumlah

        # tambah ke toko
        toko_obj.terima_barang(id_b, jumlah)
        db.data["toko"][id_t]["stok"] = toko_obj._stok

        # simpan distribusi
        dist = Distribusi(id_b, id_t, jumlah, id_g)
        db.data["distribusi"].append(dist.to_dict())

        db.save()
        print("✅ Distribusi berhasil!")

    except Exception as e:
        print(f"{Theme.FAIL}❌ {e}{Theme.ENDC}")

    input("\nEnter...")


def update_status_distribusi():
    if not db.data["distribusi"]:
        print("❌ Belum ada data distribusi!")
        input("Enter...")
        return

    print("\n=== UPDATE STATUS DISTRIBUSI ===")

    distribusi_list = [Distribusi.from_dict(d) for d in db.data["distribusi"]]

    for i, d in enumerate(distribusi_list):
        print(f"{i+1}. Barang: {d.barang} | Gudang: {d.gudang} | Toko: {d.toko}")

    try:
        pilih = int(input("Pilih nomor: ")) - 1

        if pilih < 0 or pilih >= len(distribusi_list):
            print("❌ Pilihan tidak valid!")
            return

        status = input("Status baru (dikirim/sampai/proses/tertunda): ")

        distribusi_list[pilih].update_status(status)

        db.data["distribusi"] = [d.to_dict() for d in distribusi_list]
        db.save()

        print("✅ Status berhasil diupdate!")

    except Exception as e:
        print("❌ Error:", e)

    input("\nEnter...")


def menu_laporan():
    laporan = Laporan(db.data)

    while True:
        print("\n=== MENU LAPORAN ===")
        print("1. Lihat Semua Laporan")
        print("2. Hapus Riwayat Distribusi")
        print("0. Kembali")

        pilih = input("Pilih: ")

        if pilih == "1":
            laporan.tampilkan_semua()
            input("\nEnter...")

        elif pilih == "2":
            laporan.hapus_riwayat()
            db.save()  # 🔥 WAJIB
            input("\nEnter...")

        elif pilih == "0":
            break

        else:
            print("❌ Pilihan tidak valid!")

def cek_stok_gudang():
    Laporan(db.data).tampilkan_gudang()
    input("\nEnter...")

def cek_stok_toko():
    print("\n--- STOK TOKO ---")
    for id_t, t in db.data["toko"].items():
        print(f"{t['nama']} : {t.get('stok', {})}")
    input("\nEnter...")

def jual_barang():
    id_t = input_tidak_kosong("ID Toko: ")
    id_b = input_tidak_kosong("ID Barang: ")
    jumlah = input_angka("Jumlah: ")

    try:
        toko_data = db.data["toko"][id_t]
        toko_obj = Toko(id_t, toko_data["nama"])
        toko_obj._stok = toko_data["stok"]

        toko_obj.jual_barang(id_b, jumlah)

        db.data["toko"][id_t]["stok"] = toko_obj._stok
        db.save()

    except Exception as e:
        print(f"{Theme.FAIL}❌ {e}{Theme.ENDC}")

    input("\nEnter...")

# ================= MAIN =================

def main():
    Config.display_splash()
    auth_system = Auth(db)

    user_aktif = None
    while not user_aktif:
        user_aktif = auth_system.login()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        user_aktif.tampilkan_welcome()

        akses = user_aktif.akses_menu()
        menu_map = {}

        print(f"{Theme.BOLD}MENU UTAMA:{Theme.ENDC}")

        for i, item in enumerate(akses, 1):
            menu_map[str(i)] = item
            print(f"{i}. {item}")

        pilih = input("Pilih: ")

        if pilih in menu_map:
            aksi = menu_map[pilih]

            if aksi == "keluar":
                auth_system.logout(user_aktif.nama)
                break
            elif aksi == "tambah user":
                tambah_user()
            elif aksi == "tambah barang":
                tambah_barang()
            elif aksi == "tambah gudang":
                tambah_gudang()
            elif aksi == "tambah toko":
                tambah_toko()
            elif aksi == "manajemen stok":
                manajemen_stok()
            elif aksi == "distribusi barang":
                distribusi()
            elif aksi == "laporan lengkap":
                menu_laporan()
            elif aksi == "update status distribusi":
                update_status_distribusi()
            elif aksi == "cek stok gudang":
                cek_stok_gudang()
            elif aksi == "cek stok toko":
                cek_stok_toko()
            elif aksi == "jual barang":
                jual_barang()
        else:
            print("Pilihan tidak valid")
            input("Enter...")

if __name__ == "__main__":
    main()