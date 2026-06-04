# 🚀 Quick Reference - Docker untuk Hirely AI

## ⚡ Build Image (Kecil & Cepat)
```bash
docker build -t hirely-ai:latest .
```

## 🏃 Run untuk Testing Lokal
```bash
docker run -p 7860:7860 hirely-ai:latest
```
→ Buka browser: **http://localhost:7860/docs**

---

## 📊 Build & Run Workflow

| Langkah | Perintah | Waktu |
|---------|---------|-------|
| Build | `docker build -t hirely-ai:latest .` | ~2-5 min |
| Run Background | `docker run -d -p 7860:7860 --name app hirely-ai:latest` | Instant |
| View Logs | `docker logs -f app` | Real-time |
| Stop | `docker stop app` | < 1 sec |
| Remove | `docker rm app` | < 1 sec |

---

## 🎯 Common Commands

### Build & Test Lengkap
```bash
# Build
docker build -t hirely-ai:latest .

# Run di background
docker run -d -p 7860:7860 --name hirely hirely-ai:latest

# Lihat logs
docker logs -f hirely

# Test endpoint
curl http://localhost:7860/docs

# Stop
docker stop hirely
docker rm hirely
```

### Run dengan Volume (Development)
```bash
docker run -p 7860:7860 \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/model:/app/model \
  hirely-ai:latest
```

### Rebuild Tanpa Cache
```bash
docker build --no-cache -t hirely-ai:latest .
```

### Check Image Info
```bash
docker images hirely-ai        # Size, ID, tag
docker inspect hirely-ai       # Detail metadata
```

---

## 📁 File Structure di Container

```
/app/
├── src/
│   ├── app.py              ← FastAPI app (di-expose)
│   ├── model_loader.py
│   ├── predictor.py
│   ├── schema.py
│   └── custom_layers.py
├── model/
│   ├── skill_gap_model.keras
│   ├── skill_labels.json
│   └── tfidf_vectorizer.pkl
├── requirements.txt
└── README.md
```

---

## 🔧 Dockerfile Key Points

| Aspect | Value |
|--------|-------|
| Base Image | `python:3.11-slim` |
| Build Strategy | Multi-stage (optimize size) |
| Port | 7860 (Hugging Face standard) |
| Entry Point | `uvicorn src.app:app --host 0.0.0.0 --port 7860` |
| Estimated Size | ~900 MB |
| Health Check | ✅ Yes (every 30s) |

---

## ⚙️ Environment Variables dalam Dockerfile

```dockerfile
PYTHONUNBUFFERED=1              # Direct output logging
PYTHONDONTWRITEBYTECODE=1       # Skip .pyc generation
PIP_NO_CACHE_DIR=1              # No pip caching
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 7860 already in use | `docker run -p 7861:7860 ...` |
| Container crashes | `docker logs container-name` |
| Image too large | Multi-stage build sudah optimal |
| Slow build | Use `--progress=plain` untuk info lebih |
| Container tidak start | Check Uvicorn errors di logs |

---

## 📚 Dokumentasi Lengkap

- **Penjelasan detail**: Lihat `DOCKERFILE_EXPLANATION.md`
- **Semua commands**: Lihat `DOCKERFILE_COMMANDS.md`
- **Dockerfile**: Lihat `Dockerfile`

---

## ✅ Pre-Deployment Checklist

- [ ] `requirements.txt` lengkap dengan semua dependencies
- [ ] `src/app.py` menggunakan `app = FastAPI()`
- [ ] Model files ada di `model/` folder
- [ ] Image build berhasil: `docker build -t hirely-ai:latest .`
- [ ] Container run berhasil: `docker run -p 7860:7860 hirely-ai:latest`
- [ ] Endpoint accessible: `curl http://localhost:7860/docs`
- [ ] Health check OK: `docker inspect hirely-ai`
- [ ] Siap deploy ke Hugging Face 🎉

---

## 🚀 Deploy ke Hugging Face

```bash
# Tag image
docker tag hirely-ai:latest username/hirely-ai:latest

# Push
docker push username/hirely-ai:latest

# Di Hugging Face Space, gunakan: username/hirely-ai:latest
```

---

**📞 Butuh bantuan?** Lihat:
- `DOCKERFILE_EXPLANATION.md` - Detail setiap instruksi
- `DOCKERFILE_COMMANDS.md` - Semua commands & options
- `Dockerfile` - Source file
