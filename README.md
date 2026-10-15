# Parallel File Analyzer

Proyek ini merupakan mini project Ujian Tengah Semester mata kuliah Komputasi Paralel dan Terdistribusi. Program menganalisis sekumpulan file teks dengan menggabungkan dua paradigma paralelisme di Python, yaitu **Thread Pool** untuk membaca file dan **Process Pool** untuk menganalisis isi file.

## Identitas

- **Nama:** Muhammad Nazril Putra Rosida
- **NIM:** 247006111162
- **Mata kuliah:** Komputasi Paralel dan Terdistribusi
- **Judul:** Parallel File Analyzer Menggunakan Thread Pool dan Process Pool

## Fitur

- Membuat dataset teks secara otomatis dengan seed berdasarkan NIM.
- Membaca file menggunakan `ThreadPoolExecutor`.
- Menganalisis teks menggunakan `ProcessPoolExecutor`.
- Menghitung jumlah karakter, kata, vokal, angka, dan simbol.
- Mengukur waktu eksekusi sequential dan hybrid.
- Menghitung throughput, speedup, dan efisiensi.
- Menjalankan benchmark dengan beberapa kombinasi thread, process, dan jumlah data.
- Membuat grafik hasil benchmark melalui `generate_plots.py`.

## Teknologi

- Python 3
- `concurrent.futures` untuk Thread Pool dan Process Pool
- `argparse`, `pathlib`, `time`, dan `csv` dari standard library
- `matplotlib` untuk membuat grafik benchmark

## Struktur Folder

```text
UTS/
├── dataset/
│   ├── data_0001.txt
│   ├── data_0002.txt
│   └── ...
├── generate_data.py
├── main.py
├── generate_plots.py
├── benchmark_results.csv
├── benchmark_dashboard.png
├── waktu_vs_thread.png
├── waktu_vs_process.png
└── speedup_vs_konfigurasi.png
```

File hasil seperti `benchmark_results.csv` dan grafik akan muncul setelah proses benchmark dan pembuatan grafik berhasil. Nama file grafik mengikuti konfigurasi di `generate_plots.py`.

## Persyaratan

Pastikan Python sudah terpasang. Periksa versi Python melalui terminal:

```bash
python --version
```

Jika `generate_plots.py` menggunakan Matplotlib dan library tersebut belum terpasang, jalankan:

```bash
python -m pip install matplotlib
```

## Cara Menjalankan

Jalankan perintah berikut dari terminal di folder proyek.

### 1. Membuat dataset

```bash
python generate_data.py
```

Script membuat 1.620 file teks di folder `dataset/`. Script menggunakan `random.seed(247006111162)` agar proses pembuatan data dapat direproduksi dengan seed yang sama.

### 2. Menjalankan konfigurasi utama

Konfigurasi utama yang ditentukan dari NIM adalah 4 thread, 3 process, dan 1.620 file.

```bash
python main.py --threads 4 --processes 3 --data 1620
```

Program menampilkan statistik teks, waktu sequential, waktu hybrid, throughput, speedup, dan efisiensi.

### 3. Menjalankan konfigurasi lain

Contoh pengujian dengan 2 thread, 2 process, dan 1.620 file:

```bash
python main.py --threads 2 --processes 2 --data 1620
```

Contoh pengujian dengan 3 thread dan 2 process:

```bash
python main.py --threads 3 --processes 2 --data 1620
```

Jumlah data yang diminta tidak boleh melebihi jumlah file yang tersedia di folder `dataset/`.

### 4. Menjalankan benchmark otomatis

```bash
python main.py --bench
```

Benchmark menjalankan rangkaian konfigurasi yang didefinisikan di `main.py`, lalu menyimpan hasilnya ke `benchmark_results.csv`. Pastikan folder `dataset/` sudah berisi 1.620 file sebelum menjalankan benchmark.

### 5. Membuat grafik

Setelah benchmark selesai, jalankan:

```bash
python generate_plots.py
```

Script grafik perlu membaca `benchmark_results.csv` terbaru. Jika ingin memperbarui grafik setelah pengujian ulang, jalankan benchmark terlebih dahulu, kemudian jalankan kembali script grafik.

## Parameter Personal

Parameter utama proyek dihitung dari NIM `247006111162` sesuai ketentuan UTS:

| Parameter | Perhitungan | Hasil |
|---|---|---:|
| Jumlah thread | 62 mod 4 + 2 | 4 |
| Jumlah process | 61 mod 3 + 2 | 3 |
| Jumlah data | 162 × 10 | 1.620 |

## Metrik Performa

Program menggunakan metrik berikut:

- **Waktu sequential:** waktu saat data diproses tanpa paralelisme.
- **Waktu hybrid:** waktu saat pembacaan dan analisis menggunakan Thread Pool dan Process Pool.
- **Throughput:** jumlah file dibagi waktu hybrid, dalam data per detik.
- **Speedup:** waktu sequential dibagi waktu hybrid.
- **Efisiensi:** speedup dibagi jumlah process, lalu dikali 100%.

Rumus yang digunakan:

```text
Throughput = jumlah data / waktu hybrid
Speedup = waktu sequential / waktu hybrid
Efisiensi (%) = speedup / jumlah process × 100
```

## Catatan Pengujian

- Waktu eksekusi dapat berbeda antar komputer dan antar pengulangan karena dipengaruhi CPU, RAM, storage, beban sistem, dan overhead paralelisme.
- Untuk laporan, gunakan angka dari benchmark yang benar-benar dijalankan pada komputer pengujian.
- Pastikan tabel, grafik, dan screenshot pada laporan merujuk pada file `benchmark_results.csv` yang sama.
- Periksa bahwa grafik memakai data terbaru dan tidak memuat nilai yang ditulis secara manual di dalam script.

## Lisensi

Proyek ini dibuat untuk keperluan akademik Ujian Tengah Semester.
