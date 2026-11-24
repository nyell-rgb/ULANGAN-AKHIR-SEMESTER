# UJIAN-AKHIR-SEMESTER
PRAKTIK PEMROGRAMAN DASAR
NAMA  : NATANIEL BANNE
NIM   : 266151008
KELAS : TEKNIK INFORMATIKA
DOSEN : MUHAMMAD TAUFIQ SUMADI

# Deskripsi
Aplikasi desktop berbasis GUI (Python + Tkinter) untuk membantu pemilik toko kecil
mengelola stok barang dan menghitung belanja beserta diskon secara otomatis.

# Fitur
- Tambah, ubah, dan hapus data barang (inventaris)
- Keranjang belanja dengan pengecekan stok
- Diskon bertingkat: 2% (≥ Rp100.000), 5% (≥ Rp200.000), 10% (≥ Rp500.000)
- Perhitungan total dan kembalian, stok berkurang otomatis setelah bayar
- Data tersimpan otomatis ke file `data_toko.json`
- Penanganan error untuk input yang tidak valid

# Materi yang Diterapkan
| Materi | Penerapan |
|---|---|
| Struktur data | `list` berisi `dict` untuk barang dan keranjang, `tuple` untuk kolom dan aturan diskon |
| Fungsi | Lebih dari 10 fungsi, misalnya `tambah_barang`, `hitung_total`, `proses_pembayaran` |
| Pengkondisian | Diskon bertingkat, cek stok, cek uang bayar |
| Perulangan | `for` dan `sum()` untuk mencari dan menghitung data |
| Error handling | `try/except` dan `raise ValueError` |
| File | Simpan dan muat data dengan JSON |

# Cara Menjalankan
1. Pastikan Python 3 terpasang (Tkinter sudah termasuk di Windows dan macOS).
   Di Linux: `sudo apt install python3-tk`
2. Unduh atau clone repository ini.
3. Jalankan:
   # python app_toko.py

# Cara Penggunaan
1. **Tab Inventaris:** isi kode, nama, harga, dan stok, lalu klik Tambah.
   Klik barang di tabel untuk mengubah atau menghapusnya.
2. **Tab Kasir:** pilih barang, isi jumlah, klik Tambah ke Keranjang.
3. Masukkan uang bayar, lalu klik Bayar.

