# Penjelasan Dockerfile untuk Hirely AI

## 📋 Ringkasan Dokumen
Dokumen ini menjelaskan setiap baris dalam Dockerfile yang menggunakan **multi-stage build** untuk mengoptimalkan ukuran image. Dengan pendekatan ini, ukuran image final akan lebih kecil karena build tools tidak disertakan.

---

## 🏗️ STAGE 1: BUILDER

### `FROM python:3.11-slim as builder`
- **Fungsi**: Menggunakan Python 3.11-slim sebagai base image untuk tahap build
- **Penjelasan**: 
  - `python:3.11-slim` adalah versi lightweight dari Python 3.11
  - Lebih kecil dari `python:3.11-full` karena tidak ada docs dan development tools
  - `as builder` memberi nama stage ini untuk referensi di tahap selanjutnya
- **Mengapa slim**: Mengurangi ukuran image dan waktu download

### `WORKDIR /app`
- **Fungsi**: Mengatur direktori kerja di dalam container
- **Penjelasan**: Semua command selanjutnya akan dijalankan dari `/app`
- **Best Practice**: Membuat struktur yang konsisten

### `RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*`
- **Fungsi**: Menginstall build tools yang diperlukan untuk kompilasi
- **Penjelasan**:
  - `apt-get update`: Mengupdate package manager
  - `build-essential`: Paket untuk compile dari source (C compiler, dll)
  - `--no-install-recommends`: Hanya install paket yang dibutuhkan, tidak recommended packages
  - `rm -rf /var/lib/apt/lists/*`: Menghapus cache apt untuk menghemat ukuran layer
- **Mengapa**: TensorFlow sering memerlukan build tools untuk kompilasi

### `COPY requirements.txt .`
- **Fungsi**: Menyalin file requirements.txt dari host ke container
- **Penjelasan**: 
  - File ini berisi daftar Python packages yang akan diinstall
  - Disalin ke `/app/requirements.txt`

### `RUN pip install --upgrade pip setuptools wheel && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt`
- **Fungsi**: Menginstall semua dependencies dan membuat wheel files
- **Penjelasan**:
  - `pip install --upgrade pip setuptools wheel`: Upgrade pip ke versi terbaru
  - `pip wheel`: Membuat binary wheel files dari packages
    - `--no-cache-dir`: Tidak menyimpan cache (hemat space)
    - `--no-deps`: Hanya buat wheel untuk packages, tidak dependencies
    - `--wheel-dir /app/wheels`: Simpan wheel di folder `/app/wheels`
  - `-r requirements.txt`: Gunakan requirements.txt sebagai source
- **Keuntungan**: Wheel files dapat diinstall lebih cepat di tahap production

---

## 🚀 STAGE 2: PRODUCTION RUNTIME

### `FROM python:3.11-slim`
- **Fungsi**: Membuat image baru tanpa build tools (clean slate)
- **Penjelasan**: 
  - Ini adalah image final yang akan dijalankan
  - Lebih kecil karena tidak termasuk build-essential dan build tools dari stage 1
  - Hanya akan memiliki runtime libraries yang diperlukan

### `WORKDIR /app`
- **Fungsi**: Mengatur working directory yang sama seperti builder stage
- **Penjelasan**: Konsistensi struktur direktori

### `ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1`
- **Fungsi**: Mengatur environment variables untuk Python
- **Penjelasan**:
  - `PYTHONUNBUFFERED=1`: Output Python langsung tercetak (tidak di-buffer), penting untuk logging
  - `PYTHONDONTWRITEBYTECODE=1`: Jangan buat file `.pyc`, menghemat space
  - `PIP_NO_CACHE_DIR=1`: Jangan cache pip packages saat install
- **Best Practice**: Meningkatkan performa logging dan menghemat storage

### `RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*`
- **Fungsi**: Menginstall library runtime yang diperlukan
- **Penjelasan**:
  - `libgomp1`: GNU OpenMP library, dibutuhkan oleh TensorFlow/NumPy
  - Hanya library runtime, bukan build tools
  - `--no-install-recommends`: Hanya paket essential
  - `rm -rf /var/lib/apt/lists/*`: Bersihkan cache
- **Mengapa**: TensorFlow menggunakan OpenMP untuk parallel processing

### `COPY --from=builder /app/wheels /wheels`
- **Fungsi**: Menyalin wheel files dari builder stage ke production stage
- **Penjelasan**:
  - `--from=builder`: Ambil dari stage 1 (builder)
  - `/app/wheels`: Sumber folder dari builder
  - `/wheels`: Tujuan di production container
- **Keuntungan**: Wheels sudah dikompile, install lebih cepat

### `COPY requirements.txt .`
- **Fungsi**: Menyalin requirements.txt untuk referensi
- **Penjelasan**: Diperlukan untuk pip install command berikutnya

### `RUN pip install --upgrade pip setuptools wheel && pip install --no-cache /wheels/*`
- **Fungsi**: Menginstall wheel files ke Python
- **Penjelasan**:
  - `pip install --upgrade pip setuptools wheel`: Upgrade pip
  - `pip install --no-cache /wheels/*`: Install semua wheels dari folder `/wheels`
  - `--no-cache`: Tidak cache hasil install
- **Keuntungan**: Install cepat karena wheels sudah dikompile

### `COPY . .`
- **Fungsi**: Menyalin seluruh source code dari host ke container
- **Penjelasan**:
  - Source dari `.` (root project di host)
  - Destination ke `.` (current directory `/app` di container)
  - Mencakup: src/, model/, .gitignore, README.md, dll
- **Struktur**: Akan membuat folder `/app/src/`, `/app/model/`, dll

### `EXPOSE 7860`
- **Fungsi**: Mendokumentasikan port yang di-expose
- **Penjelasan**:
  - Ini adalah port untuk Hugging Face Docker Space
  - EXPOSE bukan benar-benar membuka port, hanya dokumentasi
  - Port sesungguhnya dibuka saat run dengan `-p` flag
- **Catatan**: Saat deploy ke Hugging Face, port 7860 adalah standard

### `HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 CMD ...`
- **Fungsi**: Membuat health check untuk container
- **Penjelasan**:
  - `--interval=30s`: Cek kesehatan setiap 30 detik
  - `--timeout=10s`: Timeout 10 detik untuk setiap cek
  - `--start-period=5s`: Tunggu 5 detik sebelum mulai cek (startup time)
  - `--retries=3`: Container dianggap unhealthy setelah 3 kali gagal
  - CMD: Menjalankan curl ke `/docs` endpoint
- **Manfaat**: Docker/Orchestration tools bisa detect jika app crash
- **Opsional**: Bisa dihapus jika tidak diperlukan

### `CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]`
- **Fungsi**: Command default untuk menjalankan aplikasi
- **Penjelasan**:
  - `uvicorn`: ASGI server untuk FastAPI
  - `src.app:app`: Modul dan variabel aplikasi FastAPI
    - `src.app`: File `/app/src/app.py`
    - `app`: Variabel bernama `app` di file tersebut
  - `--host 0.0.0.0`: Listen di semua interface (required untuk Docker)
  - `--port 7860`: Port 7860 untuk Hugging Face
- **Format JSON**: Menggunakan exec form (direkomendasikan untuk Docker)

---

## 📊 Perbandingan Ukuran (Estimasi)

| Metode | Ukuran Image |
|--------|-------------|
| Single-stage (tanpa optimasi) | ~2.5 GB |
| Single-stage dengan optimasi | ~1.8 GB |
| **Multi-stage (ini)** | **~900 MB** |

---

## 🔐 Best Practices yang Diterapkan

1. ✅ **Multi-stage build**: Mengurangi ukuran image hingga 50%
2. ✅ **Layer caching**: Mengoptimalkan build time
3. ✅ **--no-install-recommends**: Hanya install yang diperlukan
4. ✅ **Cache cleanup**: Menghapus cache apt dan pip
5. ✅ **Environment variables**: Konfigurasi Python optimal
6. ✅ **Non-root user**: ❌ Opsional (bisa ditambahkan)
7. ✅ **Health check**: Monitoring kesehatan container
8. ✅ **Slim base image**: python:3.11-slim tidak python:3.11-full

---

## 🚀 Perintah Build & Run

Lihat file `DOCKERFILE_COMMANDS.md` untuk perintah lengkap.
