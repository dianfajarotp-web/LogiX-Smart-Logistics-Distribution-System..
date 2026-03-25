from config import Theme

class Laporan:
    def __init__(self, db_data):
        self.db = db_data
        self.width = 90

    def _header(self, title):
        print(f"\n{Theme.HEADER}{Theme.BOLD}{title.center(self.width)}{Theme.ENDC}")
        print(f"{Theme.OKCYAN}{'=' * self.width}{Theme.ENDC}")

    def _footer(self):
        print(f"{Theme.OKCYAN}{'=' * self.width}{Theme.ENDC}")

    def tampilkan_barang(self):
        self._header("📊 DAFTAR INVENTARIS BARANG PUSAT")

        print(f"{Theme.BOLD}{'No':<3} {'Barang':<10} {'Gudang':<10} {'Toko':<10} {'Qty':<8}{Theme.ENDC}")
        print("-" * self.width)
        if not self.db.get("barang"):
            print(f"{'Data barang masih kosong'.center(self.width)}")
        else:
            for i, d in enumerate(self.db.get("distribusi", []), 1):
                barang = d.get("barang", "-")
                gudang = d.get("gudang", "-")
                toko = d.get("toko", "-")
                jumlah = d.get("jumlah", 0)

                # ✅ Baris utama tetap rapi (kolom sejajar)
                print(f"{i:<3} {barang:<10} {gudang:<10} {toko:<10} {jumlah:<8}")

                # ✅ History ditaruh di bawah (tidak merusak tabel)
                history = d.get("history", [])

                if history:
                    for h in history:
                        print(f"{'':<5} └─ {h['status']} ({h['waktu']})")
                else:
                    print(f"{'':<5} (tidak ada riwayat)")

                print("-" * self.width)

        self._footer()

    def tampilkan_gudang(self):
        self._header("🏭 MONITORING STOK GUDANG")

        if not self.db.get("gudang"):
            print(f"{'Belum ada gudang terdaftar'.center(self.width)}")
        else:
            for id_g, g in self.db.get("gudang", {}).items():
                print(f"\n{Theme.WARNING}ID GUDANG: {id_g} | NAMA: {g.get('nama', '-')}{Theme.ENDC}")
                print(f"{'-' * 50}")

                stok_data = g.get("stok", {})

                if not stok_data:
                    print(f" {Theme.FAIL}⚠️ Gudang ini masih kosong{Theme.ENDC}")
                else:
                    print(f"{'ID BARANG':<15} {'NAMA BARANG':<25} {'JUMLAH':<10}")
                    for id_b, jumlah in stok_data.items():
                        nama_b = self.db.get("barang", {}).get(id_b, {}).get("nama", "Unknown")
                        print(f"{id_b:<15} {nama_b:<25} {jumlah:<10}")

        self._footer()

    def tampilkan_distribusi(self):
        self._header("🚚 LOG AKTIVITAS DISTRIBUSI LOGISTIK")

        print(f"{Theme.BOLD}{'PRODUK':<15} {'DARI':<15} {'KE TOKO':<15} {'QTY':<8} {'STATUS TERAKHIR':<20}{Theme.ENDC}")
        print(f"{Theme.OKCYAN}{'-' * self.width}{Theme.ENDC}")

        if not self.db.get("distribusi"):
            print(f"{'Belum ada riwayat pengiriman'.center(self.width)}")
        else:
            for d in self.db.get("distribusi", []):
                barang = d.get("barang", "-")
                gudang = d.get("gudang", "-")
                toko = d.get("toko", "-")
                jumlah = d.get("jumlah", 0)

                history = d.get("history", [])
                if history:
                    last_status = history[-1].get("status", "-")
                    last_waktu = history[-1].get("waktu", "-")
                    status_tampil = f"{last_status} ({last_waktu})"
                else:
                    status_tampil = "-"

                print(f"{barang:<15} {gudang:<15} {toko:<15} {jumlah:<8} {status_tampil:<20}")
            for h in history:
                print(f"   ↳ {h['status']} ({h['waktu']})")
        self._footer()

    def tampilkan_semua(self):
        self.tampilkan_barang()
        self.tampilkan_gudang()
        self.tampilkan_distribusi()


    def hapus_riwayat(self):
        if not self.db["distribusi"]:
            print("❌ Tidak ada riwayat distribusi!")
            return

        print("\n=== HAPUS RIWAYAT DISTRIBUSI ===")

        # tampilkan data dulu
        for i, d in enumerate(self.db["distribusi"]):
            print(f"{i+1}. Barang: {d['barang']} | Gudang: {d.get('gudang','-')} | Toko: {d['toko']} | Jumlah: {d['jumlah']}")

        try:
            pilih = int(input("Pilih nomor yang ingin dihapus: ")) - 1

            if pilih < 0 or pilih >= len(self.db["distribusi"]):
                print("❌ Pilihan tidak valid!")
                return

            konfirmasi = input("Yakin ingin hapus? (y/n): ").lower()
            if konfirmasi != "y":
                print("❌ Dibatalkan")
                return

            # hapus data
            del self.db["distribusi"][pilih]

            print("✅ Riwayat berhasil dihapus!")

        except ValueError:
            print("❌ Input harus angka!")