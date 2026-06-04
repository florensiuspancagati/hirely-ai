# # =============================================================================
# # STAGE 1: Builder (opsional - untuk optimasi ukuran image)
# # =============================================================================
# FROM python:3.11-slim as builder

# WORKDIR /app

# # Install dependencies yang diperlukan untuk build
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# # Copy requirements.txt
# COPY requirements.txt .

# # Install Python dependencies ke folder /app/wheels
# RUN pip install --upgrade pip setuptools wheel && \
#     pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# # =============================================================================
# # STAGE 2: Production Runtime
# # =============================================================================
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PIP_NO_CACHE_DIR=1

# # Install dependencies runtime saja (hapus build tools untuk optimalkan ukuran)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libgomp1 \
#     && rm -rf /var/lib/apt/lists/*

# # Copy wheels dari builder stage
# COPY --from=builder /app/wheels /wheels

# # Copy requirements.txt
# COPY requirements.txt .

# # Install dependencies dari wheels
# RUN pip install --upgrade pip setuptools wheel && \
#     pip install --no-cache /wheels/*

# # Copy seluruh source code
# COPY . .

# # Expose port untuk Hugging Face (7860)
# EXPOSE 7860

# # Health check (opsional)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#     CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/docs').read()" || exit 1

# # Run aplikasi dengan uvicorn
# CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]