# StockOps - Aplikasi Manajemen Inventaris

## Deskripsi
StockOps adalah aplikasi manajemen inventaris yang dirancang untuk membantu pengguna mengelola stok barang, melakukan analisis terhadap data inventaris, serta menampilkan informasi penting terkait stok barang. Aplikasi ini dibangun menggunakan Python dengan antarmuka pengguna berbasis Tkinter dan Matplotlib untuk visualisasi data.

## Fitur
- **CRUD (Create, Read, Update, Delete)**:
  - Tambah barang baru ke dalam database.
  - Tampilkan semua barang yang ada di dalam database.
  - Perbarui informasi barang yang ada di dalam database.
  - Hapus barang dari database.

- **Analisis Data**:
  - Tampilkan barang dengan stok terbanyak.
  - Tampilkan barang dengan harga tertinggi.
  - Tampilkan barang yang stoknya di bawah stok minimum.

## Teknologi yang Digunakan
- Python
- Tkinter (untuk GUI)
- Matplotlib (untuk visualisasi data)
- MySQL (untuk database)
- mysql-connector-python (untuk koneksi ke database MySQL)

## Instalasi
Ikuti langkah-langkah berikut untuk menginstal dan menjalankan proyek ini secara lokal:

1. Clone repositori ini:
   ```bash
   git clone https://github.com/renaldidafa/project-digitalent.git

## Fitur Aplikasi

1. Menambahkan Barang:

- Isi formulir dengan kode barang, nama, deskripsi, stok, stok minimum, dan harga.
- Klik tombol "Save" untuk menambahkan barang ke database.

2.Memperbarui Barang:
- Pilih barang yang ingin diperbarui dari tabel.
- Isi formulir dengan informasi yang diperbarui.
- Klik tombol "Update" untuk menyimpan perubahan.

3. Menghapus Barang:
- Pilih barang yang ingin dihapus dari tabel.
- Klik tombol "Delete" untuk menghapus barang dari database.

4. Analisis Data:
- Klik tombol "Analisis" untuk membuka menu analisis.
= Pilih salah satu opsi analisis untuk melihat grafik.
