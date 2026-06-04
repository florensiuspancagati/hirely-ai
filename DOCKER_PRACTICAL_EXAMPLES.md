# 🎯 Contoh Praktis Docker untuk Hirely AI

## 1️⃣ Testing Lokal (Paling Sering)

### Scenario A: Quick Test
```bash
# Build
docker build -t hirely-ai:latest .

# Run
docker run -p 7860:7860 hirely-ai:latest
```

**Hasil**:
```
INFO:     Uvicorn running on http://0.0.0.0:7860
INFO:     Application startup complete
```

**Buka di Browser**: http://localhost:7860/docs

---

### Scenario B: Background Running dengan Logs
```bash
# Run di background
docker run -d --name hirely -p 7860:7860 hirely-ai:latest

# Monitor logs
docker logs -f hirely

# Ketika selesai testing
docker stop hirely
docker rm hirely
```

---

### Scenario C: Development dengan Hot Reload
```bash
# Jika ingin auto-reload saat code changes
docker run -p 7860:7860 \
  -v $(pwd)/src:/app/src \
  --name hirely-dev \
  hirely-ai:latest
```

**Catatan**: Tergantung FastAPI config (reload=True di Uvicorn)

---

## 2️⃣ Testing dengan Custom Data

### Scenario A: Test dengan File CSV
```bash
# Buat directory untuk test data
mkdir test_data

# Copy data ke container
docker run -p 7860:7860 \
  -v $(pwd)/test_data:/app/test_data \
  --name hirely \
  hirely-ai:latest
```

**Di dalam container**:
```bash
docker exec -it hirely python -c "
import pandas as pd
df = pd.read_csv('/app/test_data/resumes.csv')
print(df.head())
"
```

---

### Scenario B: Interactive Testing
```bash
# Buka bash di container
docker run -it -p 7860:7860 \
  --name hirely \
  hirely-ai:latest \
  bash

# Dalam container (Ctrl+D untuk exit)
python
>>> from src.predictor import SkillPredictor
>>> predictor = SkillPredictor()
>>> result = predictor.predict("Python, FastAPI, Machine Learning")
>>> print(result)
```

---

## 3️⃣ Testing Endpoints

### Test dengan curl (Sederhana)
```bash
# Pastikan container running
docker run -d -p 7860:7860 --name hirely hirely-ai:latest

# Test docs endpoint
curl http://localhost:7860/docs

# Test predict endpoint (contoh)
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -d '{
    "cv_text": "5 years Python developer, FastAPI, TensorFlow, Docker"
  }'
```

---

### Test dengan Python Script
```bash
# File: test_docker_api.py
import requests
import json

BASE_URL = "http://localhost:7860"

# Test health
response = requests.get(f"{BASE_URL}/docs")
print(f"Docs accessible: {response.status_code == 200}")

# Test predict
data = {
    "cv_text": "Python, FastAPI, Machine Learning, TensorFlow"
}
response = requests.post(f"{BASE_URL}/predict", json=data)
print(f"Prediction: {response.json()}")
```

**Run**:
```bash
python test_docker_api.py
```

---

### Test dengan Postman/Insomnia
```
POST http://localhost:7860/predict
Content-Type: application/json

{
  "cv_text": "Python, FastAPI, Machine Learning"
}
```

---

## 4️⃣ Performance Testing

### Monitor Resource Usage
```bash
# Lihat real-time stats
docker stats hirely

# Output:
# CONTAINER    MEM USAGE     MEM %     CPU %
# hirely       450MB         5%        2.1%
```

---

### Load Testing dengan Apache Bench
```bash
# Install ab (Apache Bench)
# Ubuntu: sudo apt-get install apache2-utils
# Mac: brew install httpd

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 http://localhost:7860/docs
```

---

### Load Testing dengan wrk
```bash
# Install: https://github.com/wg/wrk/wiki/Installing-wrk

# Run test (30 seconds, 4 threads, 100 connections)
wrk -t4 -c100 -d30s http://localhost:7860/docs
```

---

## 5️⃣ Debugging & Troubleshooting

### Scenario A: Container Crash
```bash
# Lihat error di logs
docker logs hirely

# Contoh error:
# ModuleNotFoundError: No module named 'tensorflow'
# → Tambah ke requirements.txt dan rebuild

# Lihat detailed error
docker logs --tail 50 hirely
```

---

### Scenario B: Check Environment Variables
```bash
# Lihat env vars di container
docker run hirely-ai:latest env

# Lihat specific env var
docker run hirely-ai:latest env | grep PYTHON
```

---

### Scenario C: Check Dependencies
```bash
# List installed packages
docker run hirely-ai:latest pip list

# Check specific package
docker run hirely-ai:latest pip show tensorflow
```

---

### Scenario D: File Structure di Container
```bash
# Explore files
docker run -it hirely-ai:latest bash

# Dalam container:
ls -la /app                      # Lihat struktur
ls -la /app/src                  # Python files
ls -la /app/model                # Model files
cat /app/requirements.txt         # Dependencies
```

---

## 6️⃣ Size Optimization Tips

### Check Image Size
```bash
docker images hirely-ai

# Output:
# REPOSITORY    TAG      SIZE
# hirely-ai     latest   950MB
```

---

### Reduce Size Further (Optional)
```bash
# 1. Update Dockerfile dengan .dockerignore
# .dockerignore file:
#   __pycache__
#   .git
#   .gitignore
#   .env
#   *.pyc
#   *.pyo
#   *.egg-info

# 2. Check layer sizes
docker history hirely-ai:latest

# 3. Rebuild
docker build -t hirely-ai:latest .
```

---

## 7️⃣ Multi-Platform Build

### Build untuk berbagai architecture
```bash
# Perlu docker buildx (biasanya sudah installed)
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t hirely-ai:latest \
  --push \
  .
```

**Gunakan untuk**:
- AWS (linux/amd64)
- ARM servers (linux/arm64)
- Raspberry Pi (linux/arm/v7)

---

## 8️⃣ Production Deployment Checklist

### Pre-deployment
```bash
# 1. Build dengan specific version
docker build -t hirely-ai:v1.0.0 -t hirely-ai:latest .

# 2. Test local
docker run -p 7860:7860 hirely-ai:v1.0.0

# 3. Test endpoints
curl http://localhost:7860/docs

# 4. Check health
docker inspect hirely-ai:v1.0.0

# 5. Stop test container
docker stop $(docker ps -q)
```

---

### Deploy ke Hugging Face
```bash
# 1. Login
huggingface-cli login

# 2. Tag dengan username
docker tag hirely-ai:v1.0.0 your-username/hirely-ai:v1.0.0
docker tag hirely-ai:latest your-username/hirely-ai:latest

# 3. Push
docker push your-username/hirely-ai:v1.0.0
docker push your-username/hirely-ai:latest

# 4. Di Hugging Face Space, set image ke:
# your-username/hirely-ai:v1.0.0
```

---

## 9️⃣ Maintenance Commands

### Clean Up
```bash
# Remove stopped containers
docker container prune

# Remove dangling images
docker image prune

# Remove unused volumes
docker volume prune

# Full cleanup (⚠️ careful!)
docker system prune -a
```

---

### Update Image
```bash
# 1. Update source code / requirements.txt
# 2. Rebuild
docker build --no-cache -t hirely-ai:latest .

# 3. Stop old container
docker stop hirely

# 4. Remove old container
docker rm hirely

# 5. Run new container
docker run -d -p 7860:7860 --name hirely hirely-ai:latest

# 6. Verify
docker logs hirely
```

---

## 🔟 Real-World Scenario: Full Workflow

```bash
# === DEVELOPMENT ===
# Edit requirements.txt / code

# === BUILD ===
docker build -t hirely-ai:dev .

# === TEST ===
docker run -d -p 7860:7860 --name test-hirely hirely-ai:dev
sleep 2
curl http://localhost:7860/docs
docker logs test-hirely

# === VERIFY ===
docker stats test-hirely &

# === CLEANUP ===
docker stop test-hirely
docker rm test-hirely

# === PRODUCTION ===
docker build -t hirely-ai:v1.0.0 -t hirely-ai:latest .
docker tag hirely-ai:v1.0.0 yourusername/hirely-ai:v1.0.0
docker push yourusername/hirely-ai:v1.0.0

# === DEPLOY ===
# Di Hugging Face Space, update image ke:
# yourusername/hirely-ai:v1.0.0
```

---

## 📊 Expected Output Saat Running

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:7860 (Press CTRL+C to quit)

# Saat ada request:
INFO:     127.0.0.1:12345 - "POST /predict HTTP/1.1" 200 OK
INFO:     127.0.0.1:12346 - "GET /docs HTTP/1.1" 200 OK
```

---

## 🎓 Tips & Best Practices

1. **Jangan rebuild setiap test** - Gunakan cached layers
2. **Gunakan .dockerignore** - Exclude unnecessary files
3. **Volume mounting untuk dev** - Faster iteration
4. **Tag dengan version** - Easy rollback
5. **Health check** - Automatic failure detection
6. **Monitor resources** - Prevent memory leaks
7. **Clean up regularly** - Save disk space
8. **Test locally first** - Before production deploy

---

## ❓ FAQ

### Q: Berapa lama build?
A: First build: ~2-5 menit (download dependencies). Subsequent builds: 30 detik (cache).

### Q: Port 7860 sudah dipakai?
A: `docker run -p 7861:7860 hirely-ai:latest` (gunakan port lain)

### Q: Bagaimana jika requirements.txt berubah?
A: `docker build --no-cache -t hirely-ai:latest .` (force rebuild)

### Q: Bisa test tanpa Docker?
A: Ya, tapi Docker memastikan consistency (sama di local dan production)

### Q: Bagaimana jika model terlalu besar?
A: Gunakan model compression atau upload ke cloud storage terlebih dahulu

---

**Butuh bantuan lebih lanjut?**
- Lihat `Dockerfile` untuk source
- Lihat `DOCKERFILE_EXPLANATION.md` untuk detail
- Lihat `DOCKERFILE_COMMANDS.md` untuk semua commands
