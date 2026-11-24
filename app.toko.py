"""
UAS Praktek Pemrograman Dasar - Politeknik Negeri Samarinda
Proyek Mikro : Aplikasi Kasir & Inventaris Toko Kecil (GUI Tkinter)

Materi yang diterapkan:
1. Struktur data  = list, dictionary, tuple
2. Fungsi         = logika program dipisah dalam fungsi-fungsi
3. Pengkondisian  = validasi input, stok, diskon bertingkat (if/elif/else)
4. Perulangan     = for / sum() / generator
5. Error handling = try / except / raise
6. File           = simpan & muat data (JSON)
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox

FILE_DATA = "data_toko.json"

# Tuple: kolom tabel (data tetap yang tidak berubah)
KOLOM_INVENTARIS = ("kode", "nama", "harga", "stok")
KOLOM_KERANJANG = ("kode", "nama", "harga", "jumlah", "subtotal")

# Tuple of tuple: aturan diskon (batas minimal belanja, persen diskon)
ATURAN_DISKON = ((500_000, 10), (200_000, 5), (100_000, 2))


# =====================================================================
# BAGIAN 1 : FUNGSI LOGIKA (tidak bergantung pada GUI)
# =====================================================================
def data_awal():
    """Data contoh jika file belum ada. List berisi dictionary."""
    return [
        {"kode": "B001", "nama": "Beras 5 Kg", "harga": 68000, "stok": 20},
        {"kode": "B002", "nama": "Minyak Goreng 1 L", "harga": 18000, "stok": 30},
        {"kode": "B003", "nama": "Gula Pasir 1 Kg", "harga": 16000, "stok": 25},
        {"kode": "B004", "nama": "Telur 1 Kg", "harga": 29000, "stok": 15},
        {"kode": "B005", "nama": "Mie Instan", "harga": 3500, "stok": 100},
    ]


def muat_data():
    """Membaca data dari file JSON. Jika gagal, pakai data awal."""
    try:
        with open(FILE_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return data_awal()


def simpan_data(inventaris):
    """Menyimpan data inventaris ke file JSON."""
    with open(FILE_DATA, "w", encoding="utf-8") as f:
        json.dump(inventaris, f, indent=4, ensure_ascii=False)


def validasi_angka(teks, nama_field, minimal=0):
    """Mengubah teks menjadi bilangan bulat dan memeriksa validitasnya."""
    try:
        angka = int(str(teks).strip())
    except ValueError:
        raise ValueError(f"{nama_field} harus berupa angka bulat.")
    if angka < minimal:
        raise ValueError(f"{nama_field} tidak boleh kurang dari {minimal}.")
    return angka


def cari_barang(inventaris, kode):
    """Mencari barang berdasarkan kode. Mengembalikan dict atau None."""
    kode = kode.strip().upper()
    for barang in inventaris:
        if barang["kode"] == kode:
            return barang
    return None


def tambah_barang(inventaris, kode, nama, harga, stok):
    """Menambah barang baru ke inventaris."""
    kode = kode.strip().upper()
    nama = nama.strip()
    if not kode or not nama:
        raise ValueError("Kode dan nama barang tidak boleh kosong.")
    if cari_barang(inventaris, kode):
        raise ValueError(f"Kode {kode} sudah digunakan.")
    inventaris.append({
        "kode": kode,
        "nama": nama,
        "harga": validasi_angka(harga, "Harga", 1),
        "stok": validasi_angka(stok, "Stok", 0),
    })


def ubah_barang(inventaris, kode, nama, harga, stok):
    """Mengubah data barang yang sudah ada."""
    barang = cari_barang(inventaris, kode)
    if barang is None:
        raise ValueError("Barang tidak ditemukan.")
    if not nama.strip():
        raise ValueError("Nama barang tidak boleh kosong.")
    barang["nama"] = nama.strip()
    barang["harga"] = validasi_angka(harga, "Harga", 1)
    barang["stok"] = validasi_angka(stok, "Stok", 0)


def hapus_barang(inventaris, kode):
    """Menghapus barang dari inventaris."""
    barang = cari_barang(inventaris, kode)
    if barang is None:
        raise ValueError("Barang tidak ditemukan.")
    inventaris.remove(barang)


def tambah_ke_keranjang(inventaris, keranjang, kode, jumlah):
    """Memasukkan barang ke keranjang setelah memeriksa stok."""
    barang = cari_barang(inventaris, kode)
    if barang is None:
        raise ValueError("Barang tidak ditemukan.")
    jumlah = validasi_angka(jumlah, "Jumlah", 1)

    # Hitung jumlah yang sudah ada di keranjang untuk barang yang sama
    item = next((i for i in keranjang if i["kode"] == barang["kode"]), None)
    sudah_ada = item["jumlah"] if item else 0

    if sudah_ada + jumlah > barang["stok"]:
        raise ValueError(
            f"Stok {barang['nama']} tidak cukup. Tersisa {barang['stok']}, "
            f"di keranjang {sudah_ada}."
        )
    if item:
        item["jumlah"] += jumlah
    else:
        keranjang.append({
            "kode": barang["kode"],
            "nama": barang["nama"],
            "harga": barang["harga"],
            "jumlah": jumlah,
        })


def hitung_diskon(subtotal):
    """Diskon bertingkat berdasarkan total belanja (pengkondisian)."""
    for batas, persen in ATURAN_DISKON:
        if subtotal >= batas:
            return persen
    return 0


def hitung_total(keranjang):
    """Mengembalikan tuple (subtotal, persen_diskon, nominal_diskon, total)."""
    subtotal = sum(i["harga"] * i["jumlah"] for i in keranjang)
    persen = hitung_diskon(subtotal)
    nominal = subtotal * persen // 100
    return subtotal, persen, nominal, subtotal - nominal


def proses_pembayaran(inventaris, keranjang, bayar):
    """Memproses pembayaran, mengurangi stok, dan mengembalikan kembalian."""
    if not keranjang:
        raise ValueError("Keranjang masih kosong.")
    bayar = validasi_angka(bayar, "Uang bayar", 0)
    total = hitung_total(keranjang)[3]
    if bayar < total:
        raise ValueError(f"Uang kurang Rp {total - bayar:,}.".replace(",", "."))
    for item in keranjang:
        cari_barang(inventaris, item["kode"])["stok"] -= item["jumlah"]
    return bayar - total


def rupiah(angka):
    """Format angka menjadi Rp 1.000.000."""
    return "Rp " + f"{angka:,}".replace(",", ".")


# =====================================================================
# BAGIAN 2 : ANTARMUKA GUI (Tkinter)
# =====================================================================
class AplikasiToko:
    def __init__(self, root):
        self.root = root
        self.root.title("Kasir & Inventaris Toko - UAS Pemrograman Dasar")
        self.root.geometry("820x560")

        self.inventaris = muat_data()
        self.keranjang = []

        tab = ttk.Notebook(root)
        self.tab_kasir = ttk.Frame(tab)
        self.tab_stok = ttk.Frame(tab)
        tab.add(self.tab_kasir, text="  Kasir  ")
        tab.add(self.tab_stok, text="  Inventaris  ")
        tab.pack(fill="both", expand=True, padx=8, pady=8)

        self.buat_tab_inventaris()
        self.buat_tab_kasir()
        self.refresh_inventaris()
        root.protocol("WM_DELETE_WINDOW", self.keluar)

    # ---------------- helper ----------------
    def buat_tabel(self, parent, kolom, lebar, tinggi=10):
        tabel = ttk.Treeview(parent, columns=kolom, show="headings", height=tinggi)
        for k, l in zip(kolom, lebar):
            tabel.heading(k, text=k.capitalize())
            tabel.column(k, width=l, anchor="w" if k == "nama" else "center")
        tabel.pack(fill="both", expand=True, padx=8, pady=6)
        return tabel

    def error(self, e):
        messagebox.showwarning("Peringatan", str(e))

    # ---------------- tab inventaris ----------------
    def buat_tab_inventaris(self):
        form = ttk.LabelFrame(self.tab_stok, text="Data Barang")
        form.pack(fill="x", padx=8, pady=6)

        self.var_kode = tk.StringVar()
        self.var_nama = tk.StringVar()
        self.var_harga = tk.StringVar()
        self.var_stok = tk.StringVar()

        isian = (("Kode", self.var_kode), ("Nama", self.var_nama),
                 ("Harga", self.var_harga), ("Stok", self.var_stok))
        for i, (label, var) in enumerate(isian):
            ttk.Label(form, text=label).grid(row=0, column=i * 2, padx=4, pady=6)
            ttk.Entry(form, textvariable=var, width=14).grid(row=0, column=i * 2 + 1, padx=4)

        tombol = ttk.Frame(self.tab_stok)
        tombol.pack(fill="x", padx=8)
        ttk.Button(tombol, text="Tambah", command=self.aksi_tambah).pack(side="left", padx=4)
        ttk.Button(tombol, text="Ubah", command=self.aksi_ubah).pack(side="left", padx=4)
        ttk.Button(tombol, text="Hapus", command=self.aksi_hapus).pack(side="left", padx=4)
        ttk.Button(tombol, text="Bersihkan", command=self.bersihkan_form).pack(side="left", padx=4)

        self.tabel_stok = self.buat_tabel(self.tab_stok, KOLOM_INVENTARIS, (90, 300, 130, 90))
        self.tabel_stok.bind("<<TreeviewSelect>>", self.pilih_barang)

    def refresh_inventaris(self):
        self.tabel_stok.delete(*self.tabel_stok.get_children())
        for b in self.inventaris:
            self.tabel_stok.insert("", "end", values=(b["kode"], b["nama"], b["harga"], b["stok"]))
        self.combo_barang["values"] = [f"{b['kode']} - {b['nama']}" for b in self.inventaris]

    def pilih_barang(self, _event=None):
        pilihan = self.tabel_stok.selection()
        if pilihan:
            kode, nama, harga, stok = self.tabel_stok.item(pilihan[0])["values"]
            self.var_kode.set(kode)
            self.var_nama.set(nama)
            self.var_harga.set(harga)
            self.var_stok.set(stok)

    def bersihkan_form(self):
        for v in (self.var_kode, self.var_nama, self.var_harga, self.var_stok):
            v.set("")

    def aksi_tambah(self):
        try:
            tambah_barang(self.inventaris, self.var_kode.get(), self.var_nama.get(),
                          self.var_harga.get(), self.var_stok.get())
        except ValueError as e:
            return self.error(e)
        simpan_data(self.inventaris)
        self.refresh_inventaris()
        self.bersihkan_form()

    def aksi_ubah(self):
        try:
            ubah_barang(self.inventaris, self.var_kode.get(), self.var_nama.get(),
                        self.var_harga.get(), self.var_stok.get())
        except ValueError as e:
            return self.error(e)
        simpan_data(self.inventaris)
        self.refresh_inventaris()

    def aksi_hapus(self):
        kode = self.var_kode.get()
        if not messagebox.askyesno("Konfirmasi", f"Hapus barang {kode}?"):
            return
        try:
            hapus_barang(self.inventaris, kode)
        except ValueError as e:
            return self.error(e)
        simpan_data(self.inventaris)
        self.refresh_inventaris()
        self.bersihkan_form()

    # ---------------- tab kasir ----------------
    def buat_tab_kasir(self):
        atas = ttk.LabelFrame(self.tab_kasir, text="Pilih Barang")
        atas.pack(fill="x", padx=8, pady=6)

        self.combo_barang = ttk.Combobox(atas, width=40, state="readonly")
        self.combo_barang.grid(row=0, column=0, padx=6, pady=8)
        ttk.Label(atas, text="Jumlah").grid(row=0, column=1)
        self.var_jumlah = tk.StringVar(value="1")
        ttk.Entry(atas, textvariable=self.var_jumlah, width=6).grid(row=0, column=2, padx=6)
        ttk.Button(atas, text="Tambah ke Keranjang", command=self.aksi_keranjang).grid(row=0, column=3, padx=6)

        self.tabel_keranjang = self.buat_tabel(self.tab_kasir, KOLOM_KERANJANG, (80, 280, 100, 80, 120), 9)

        bawah = ttk.Frame(self.tab_kasir)
        bawah.pack(fill="x", padx=8, pady=4)
        self.lbl_ringkasan = ttk.Label(bawah, text="", font=("Segoe UI", 10, "bold"), justify="left")
        self.lbl_ringkasan.pack(side="left")

        kanan = ttk.Frame(bawah)
        kanan.pack(side="right")
        ttk.Label(kanan, text="Uang Bayar").grid(row=0, column=0, padx=4)
        self.var_bayar = tk.StringVar()
        ttk.Entry(kanan, textvariable=self.var_bayar, width=14).grid(row=0, column=1, padx=4)
        ttk.Button(kanan, text="Bayar", command=self.aksi_bayar).grid(row=0, column=2, padx=4)
        ttk.Button(kanan, text="Kosongkan", command=self.kosongkan_keranjang).grid(row=0, column=3, padx=4)
        self.refresh_keranjang()

    def refresh_keranjang(self):
        self.tabel_keranjang.delete(*self.tabel_keranjang.get_children())
        for i in self.keranjang:
            self.tabel_keranjang.insert("", "end", values=(
                i["kode"], i["nama"], i["harga"], i["jumlah"], i["harga"] * i["jumlah"]))
        subtotal, persen, nominal, total = hitung_total(self.keranjang)
        self.lbl_ringkasan.config(text=(
            f"Subtotal : {rupiah(subtotal)}\n"
            f"Diskon {persen}% : {rupiah(nominal)}\n"
            f"TOTAL    : {rupiah(total)}"))

    def aksi_keranjang(self):
        pilihan = self.combo_barang.get()
        if not pilihan:
            return self.error("Pilih barang terlebih dahulu.")
        kode = pilihan.split(" - ")[0]
        try:
            tambah_ke_keranjang(self.inventaris, self.keranjang, kode, self.var_jumlah.get())
        except ValueError as e:
            return self.error(e)
        self.var_jumlah.set("1")
        self.refresh_keranjang()

    def kosongkan_keranjang(self):
        self.keranjang.clear()
        self.refresh_keranjang()

    def aksi_bayar(self):
        total = hitung_total(self.keranjang)[3]
        try:
            kembalian = proses_pembayaran(self.inventaris, self.keranjang, self.var_bayar.get())
        except ValueError as e:
            return self.error(e)
        simpan_data(self.inventaris)
        messagebox.showinfo("Transaksi Berhasil",
                            f"Total     : {rupiah(total)}\n"
                            f"Dibayar   : {rupiah(int(self.var_bayar.get()))}\n"
                            f"Kembalian : {rupiah(kembalian)}")
        self.keranjang.clear()
        self.var_bayar.set("")
        self.refresh_keranjang()
        self.refresh_inventaris()

    def keluar(self):
        simpan_data(self.inventaris)
        self.root.destroy()


def main():
    root = tk.Tk()
    AplikasiToko(root)
    root.mainloop()


if __name__ == "__main__":
    main()