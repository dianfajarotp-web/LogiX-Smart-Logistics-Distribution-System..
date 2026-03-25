# 🚀 LogiX: Smart Logistics Distribution System
LogiX adalah aplikasi manajemen logistik berbasis Python yang dirancang untuk mengelola inventaris, gudang, toko, serta distribusi barang secara terintegrasi. Sistem ini dibangun menggunakan konsep **Object-Oriented Programming (OOP)** dengan penerapan prinsip **enkapsulasi, abstraksi, inheritance, polymorphism, dan modularitas**.

## 📌 Deskripsi Singkat
Aplikasi ini memungkinkan pengguna untuk:
- Mengelola data barang, gudang, dan toko
- Melakukan distribusi barang dari gudang ke toko
- Mengontrol stok secara real-time
- Mencatat riwayat distribusi barang
- Menghasilkan laporan aktivitas logistik
- 
## 👥 Role Pengguna
Sistem memiliki beberapa peran (role), yaitu:
- **Supervisor**
  - Akses penuh ke seluruh sistem
- **Staff Gudang**
  - Mengelola stok dan gudang
- **Staff Toko**
  - Mengelola stok toko dan penjualan

## ⚙️ Fitur Utama
- ✅ Manajemen data barang
- 🏭 Manajemen gudang
- 🏪 Manajemen toko
- 🚚 Distribusi barang antar lokasi
- 📊 Laporan lengkap (stok & distribusi)
- 🔐 Sistem login berbasis role
- 🧾 Penyimpanan data menggunakan JSON

## 🧠 Konsep OOP yang Digunakan
### 1. Enkapsulasi
- Atribut menggunakan akses terbatas (`_private`)
- Data hanya dimodifikasi melalui method (getter/setter)
### 2. Abstraksi
- Menggunakan **Abstract Base Class (`User`)**
- Method `akses_menu()` wajib diimplementasikan oleh subclass
### 3. Inheritance
- `Supervisor`, `StaffGudang`, dan `StaffToko` mewarisi class `User`
### 4. Polymorphism
- Method `akses_menu()` memiliki perilaku berbeda di setiap role
### 5. Mixins
- `LogMixin` → untuk logging aktivitas
- `TimestampMixin` → untuk pencatatan waktu otomatis

## 🗂️ Struktur Project
├── main.py
├── auth.py
├── database.py
├── config.py
├── barang.py
├── gudang.py
├── toko.py
├── distribusi.py
├── laporan.py
├── user.py
├── admin.py
├── staff_gudang.py
├── staff_toko.py
├── mixins.py
├── db.json

##👨‍💻 Tim Pengembang
### 1. Dian Fajar
### 2. Fatimah Azzahra
### 3. Ghenia Fadiya Zahra
### 4. R. Daffa
