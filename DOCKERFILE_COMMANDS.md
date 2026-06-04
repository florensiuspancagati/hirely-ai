# Perintah Build & Run Docker untuk Hirely AI

## 📦 PERINTAH BUILD

### 1. Build Image (Basic)
```bash
docker build -t hirely-ai:latest .
```

**Penjelasan**:
- `docker build`: Perintah untuk build image dari Dockerfile
- `-t hirely-ai:latest`: Tag image dengan nama `hirely-ai` dan versi `latest`
- `.`: Path ke Dockerfile (current directory)

**Output**:
```
Step 1/20 : FROM python:3.11-slim as builder
...
Successfully tagged hirely-ai:latest
```

---

### 2. Build dengan Version Tag
```bash
docker build -t hirely-ai:1.0.0 -t hirely-ai:latest .
```

**Penjelasan**:
- Membuat dua tag untuk image: `1.0.0` dan `latest`
- Berguna untuk version control

---

### 3. Build dengan Progress Output
```bash
docker build --progress=plain -t hirely-ai:latest .
```

**Penjelasan**:
- `--progress=plain`: Menampilkan output plain (lebih readable)
- Alternatif: `--progress=tty` (colorful), `--progress=auto` (default)

---

### 4. Build tanpa Cache (Force Rebuild)
```bash
docker build --no-cache -t hirely-ai:latest .
```

**Penjelasan**:
- `--no-cache`: Tidak menggunakan cached layers
- Berguna jika Anda update dependencies atau source code
- Build akan lebih lambat

---

### 5. Build untuk Multiple Platforms (Advanced)
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t hirely-ai:latest .
```

**Penjelasan**:
- `docker buildx`: Extended build dengan multi-platform support
- `--platform`: Specify target architectures
- Berguna untuk deployment di berbagai cloud platforms

**Catatan**: Memerlukan `docker buildx` (biasanya sudah installed di Docker Desktop)

---

## 🏃 PERINTAH RUN

### 1. Run Container Basic
```bash
docker run -p 7860:7860 hirely-ai:latest
```

**Penjelasan**:
- `docker run`: Membuat dan menjalankan container
- `-p 7860:7860`: Port mapping (host:container)
  - Port 7860 di host → Port 7860 di container
- `hirely-ai:latest`: Image yang dijalankan

**Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:7860
INFO:     Application startup complete
```

**Akses aplikasi**: http://localhost:7860/docs

---

### 2. Run dengan Custom Container Name
```bash
docker run --name hirely-container -p 7860:7860 hirely-ai:latest
```

**Penjelasan**:
- `--name hirely-container`: Memberikan nama ke container
- Lebih mudah untuk management (stop, logs, exec, dll)

---

### 3. Run in Background (Detached Mode)
```bash
docker run -d --name hirely-container -p 7860:7860 hirely-ai:latest
```

**Penjelasan**:
- `-d`: Detached mode (background)
- Container berjalan di background, prompt kembali ke terminal

**Lihat logs**:
```bash
docker logs -f hirely-container
```

---

### 4. Run dengan Environment Variables
```bash
docker run -p 7860:7860 \
  -e LOG_LEVEL=INFO \
  -e ENV=production \
  hirely-ai:latest
```

**Penjelasan**:
- `-e`: Set environment variable
- Dapat diakses di aplikasi via `os.getenv('LOG_LEVEL')`

---

### 5. Run dengan Volume Mounting (untuk Development)
```bash
docker run -p 7860:7860 \
  -v $(pwd)/model:/app/model \
  -v $(pwd)/src:/app/src \
  hirely-ai:latest
```

**Penjelasan**:
- `-v`: Mount folder dari host ke container
- `$(pwd)`: Current directory (host)
- Berguna untuk development (real-time code updates)
- ⚠️ Tidak untuk production

**Catatan Windows PowerShell**:
```powershell
docker run -p 7860:7860 `
  -v ${PWD}/model:/app/model `
  -v ${PWD}/src:/app/src `
  hirely-ai:latest
```

---

### 6. Run dengan Resource Limits
```bash
docker run -p 7860:7860 \
  --memory=2g \
  --cpus=2 \
  hirely-ai:latest
```

**Penjelasan**:
- `--memory=2g`: Limit memory ke 2 GB
- `--cpus=2`: Limit CPU cores ke 2
- Berguna untuk mencegah container menghabiskan resources

---

### 7. Run dengan Custom Log Driver
```bash
docker run -p 7860:7860 \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  hirely-ai:latest
```

**Penjelasan**:
- Mengatur log rotation
- `max-size=10m`: Rotate log jika size > 10MB
- `max-file=3`: Simpan maksimal 3 log files

---

### 8. Run Interactive Mode (untuk Testing/Debugging)
```bash
docker run -it -p 7860:7860 \
  --name hirely-container \
  hirely-ai:latest
```

**Penjelasan**:
- `-i`: Interactive (keep STDIN open)
- `-t`: Allocate pseudo-TTY
- Berguna untuk development dan debugging

**Keluar**: Tekan `Ctrl+C`

---

## 🧪 TESTING COMMANDS

### 1. Check jika Container Berjalan
```bash
docker ps
```

**Output**:
```
CONTAINER ID   IMAGE             STATUS          PORTS
abcd1234...    hirely-ai:latest  Up 5 seconds    0.0.0.0:7860->7860/tcp
```

---

### 2. Lihat Logs
```bash
docker logs -f hirely-container
```

**Penjelasan**:
- `-f`: Follow mode (live logs)
- Tekan `Ctrl+C` untuk exit

---

### 3. Test Endpoint dengan curl
```bash
# Akses docs
curl http://localhost:7860/docs

# Health check
curl http://localhost:7860/health

# Predict endpoint (contoh)
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{"cv_text": "Python, FastAPI, Machine Learning"}'
```

---

### 4. Exec Command di Container
```bash
docker exec -it hirely-container bash
```

**Penjelasan**:
- Membuka bash shell di dalam container yang sedang berjalan
- Berguna untuk debugging atau checking logs

---

### 5. Stop Container
```bash
docker stop hirely-container
```

---

### 6. Remove Container
```bash
docker rm hirely-container
```

---

### 7. View Image Details
```bash
docker images hirely-ai
```

**Output**:
```
REPOSITORY     TAG       IMAGE ID       SIZE
hirely-ai      latest    abc123def...   950MB
```

---

## 🔄 WORKFLOW LENGKAP (Build → Run → Test)

```bash
# 1. Build image
docker build -t hirely-ai:latest .

# 2. Run container di background
docker run -d -p 7860:7860 --name hirely hirely-ai:latest

# 3. Tunggu beberapa detik untuk startup
sleep 3

# 4. Check logs
docker logs hirely

# 5. Test endpoint
curl http://localhost:7860/docs

# 6. Stop container (jika testing selesai)
docker stop hirely

# 7. Remove container
docker rm hirely
```

---

## 🐛 TROUBLESHOOTING

### Image Terlalu Besar
```bash
# Check image size
docker images hirely-ai

# Clean up dangling images
docker image prune

# Remove image dan rebuild
docker rmi hirely-ai:latest
docker build --no-cache -t hirely-ai:latest .
```

### Container Tidak Bisa Diakses
```bash
# Check jika container running
docker ps

# Check logs untuk error
docker logs hirely-container

# Verify port mapping
docker port hirely-container
```

### Memory/CPU Issues
```bash
# Monitor resource usage
docker stats hirely-container

# Update container limits
docker run -p 7860:7860 --memory=3g --cpus=4 hirely-ai:latest
```

### Rebuild Cepat (Cache)
```bash
# Jika hanya source code berubah, build akan cepat
docker build -t hirely-ai:latest .

# Jika dependency berubah (requirements.txt), build lebih lambat
docker build --no-cache -t hirely-ai:latest .
```

---

## 📝 NOTES

- **Port 7860**: Default untuk Hugging Face Spaces
- **Volume mapping**: Gunakan `-v` untuk development, jangan untuk production
- **Multi-stage build**: Mengurangi ukuran image ~50-70%
- **Health check**: Membantu orchestration tools detect failures
- **Environment variables**: Setup via `-e` flag saat run

---

## 🚀 DEPLOYMENT KE HUGGING FACE

```bash
# Login ke Hugging Face Hub
huggingface-cli login

# Build image
docker build -t hirely-ai:latest .

# Tag untuk Hugging Face
docker tag hirely-ai:latest your-username/hirely-ai:latest

# Push ke Hugging Face
docker push your-username/hirely-ai:latest
```

Kemudian di Hugging Face Space, set Docker image ke `your-username/hirely-ai:latest`

---

## ✅ CHECKLIST

- [ ] Dockerfile sudah dibuat
- [ ] requirements.txt sudah lengkap
- [ ] src/app.py sudah menggunakan `app = FastAPI()`
- [ ] Model files ada di folder `model/`
- [ ] Image berhasil di-build
- [ ] Container berhasil di-run
- [ ] Endpoint dapat diakses di `http://localhost:7860/docs`
- [ ] Health check berhasil
- [ ] Ready untuk deploy ke Hugging Face
