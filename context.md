# PROJECT OVERVIEW

## Nama Proyek
**Hirely AI** - AI-powered CV to Job Description Matching System

## Tujuan Proyek
Menganalisis kecocokan CV dengan Job Description (JD) menggunakan deep learning neural network, serta mengidentifikasi skill gap antara CV dan JD sehingga dapat memberikan rekomendasi skill yang perlu dikembangkan.

## Arsitektur Proyek
1. **Frontend**: Node.js backend (belum terintegrasi)
2. **ML Service**: FastAPI Python (dalam tahap development)
3. **Model**: TensorFlow Keras dengan custom attention layer
4. **Vectorization**: TF-IDF Vectorizer dari scikit-learn

Alur: Node.js Backend → FastAPI Service → TensorFlow Model → Analysis Result → Response

## Teknologi yang Digunakan
- **Framework**: FastAPI, Uvicorn
- **ML Libraries**: TensorFlow/Keras, scikit-learn, NumPy
- **Data Processing**: joblib (model loading), Pydantic (request validation)
- **Language**: Python 3.x
- **Dependencies**: Lihat `src/requirements.txt`

---

# FOLDER STRUCTURE

## `/model/`
**Fungsi**: Menyimpan trained model dan artifacts yang diperlukan untuk inference.

### File-file penting:
- `skill_gap_model.keras`: Pre-trained TensorFlow Keras model untuk prediksi matching antara CV dan JD
  - Menggunakan custom layer `SkillAttentionLayer`
  - Input: TF-IDF vectorized text (float32)
  - Output: Single probability value (0-1)
  - Architecture: Dense layers dengan attention mechanism

- `tfidf_vectorizer.pkl`: Pre-trained TF-IDF vectorizer dari scikit-learn
  - Mengkonversi raw text menjadi sparse feature vectors
  - Dikombinasikan untuk CV + JD
  - Ditransform ke dense array sebelum model inference

- `skill_labels.json`: List dari 28 predefined skills yang digunakan untuk skill extraction
  - Skills: agile, aws, communication, css, cyber security, devops, django, docker, ethical hacking, flask, git, html, jira, linux, marketing, mongodb, mysql, nodejs, penetration testing, photoshop, postgresql, python, react, scrum, seo, sql, ui, ux

## `/src/`
**Fungsi**: Berisi source code aplikasi Python dengan logika ML dan API.

### File-file penting:

- **`app.py`**: Entry point FastAPI application
  - Loading model, vectorizer, dan skill labels
  - **STATUS**: Hanya berisi setup, belum ada HTTP endpoint yang didefinisikan
  - **TODO**: Perlu menambahkan route/endpoint untuk handle analysis requests

- **`custom_layers.py`**: Custom Keras layer untuk attention mechanism
  - `SkillAttentionLayer`: Belajar memberi bobot pada fitur TF-IDF yang relevan
  - Units: 64 (configurable)
  - Activation: tanh + linear dengan softmax attention

- **`predictor.py`**: Core logic untuk prediction dan skill analysis
  - `clean_text()`: Membersihkan text (lowercase, remove URL, email, special chars)
  - `extract_cv_skills()`: Ekstrak skills dari teks yang ditemukan di skill_labels
  - `predict_match()`: Prediksi matching probability antara CV dan JD
  - `compute_skill_gap()`: Hitung skill gap dan matched skills
  - `generate_recommendations()`: Generate rekomendasi skill yang perlu dipelajari
  - `analyze_cv()`: Orchestrator function yang memanggil semua fungsi di atas

- **`schema.py`**: Pydantic data models untuk request/response validation
  - `AnalysisRequest`: Request model dengan fields:
    - `cv_text` (required): CV content
    - `job_description` (required): Job Description content
    - `fullname`, `position`, `education`, `experience`, `skill` (optional)

- **`model_loader.py`**: Standalone model loading script
  - Demonstrasi cara load model dengan custom objects
  - Verifikasi model dapat di-load dengan sempurna
  - **NOTE**: Code ini duplikat dengan logic di app.py

- **`requirements.txt`**: Python dependencies list
  - fastapi, uvicorn, tensorflow, numpy, scikit-learn, joblib, pydantic

- **`test_predictor.py`**: Unit test untuk predictor functions
  - Test dengan 3 dummy scenarios:
    1. Normal CV match
    2. Completely mismatched CV (Photographer vs Backend Dev)
    3. Perfect match CV
  - Print hasil match_result dan gap_result

- **`test_predict.py`**: Integration test untuk model inference
  - Test loading model dan vectorizer
  - Test prediction dengan sample text
  - Print prediction shape dan score

- **`__pycache__/`**: Python bytecode cache

## `/note.txt`
**Fungsi**: Catatan dependencies yang digunakan dan alasan penggunaan masing-masing.

---

# CURRENT IMPLEMENTATION

## Fitur yang Sudah Selesai

### 1. **Model & Vectorizer Loading** ✅
- File: `app.py`, `model_loader.py`
- Model (`skill_gap_model.keras`) dapat di-load dengan custom layer `SkillAttentionLayer`
- Vectorizer (`tfidf_vectorizer.pkl`) dapat di-load menggunakan joblib
- Skill labels (`skill_labels.json`) dapat di-load sebagai JSON

### 2. **Text Cleaning** ✅
- File: `predictor.py` → `clean_text()`
- Lowercase conversion
- Remove URLs dan emails
- Remove special characters (keep hanya alphanumeric dan space)
- Normalize whitespace

### 3. **Skill Extraction** ✅
- File: `predictor.py` → `extract_cv_skills()`
- Extract skills dari teks yang ditemukan di skill_labels
- Case-insensitive matching
- Return sorted list

### 4. **CV-JD Matching Prediction** ✅
- File: `predictor.py` → `predict_match()`
- Combine cleaned CV + JD text
- TF-IDF vectorization
- Model inference untuk probability
- Threshold-based classification (default: 0.45)
- Return: match_probability, is_match, score (%)

### 5. **Skill Gap Analysis** ✅
- File: `predictor.py` → `compute_skill_gap()`
- Identify CV skills (yang dimiliki)
- Identify JD skills (yang dibutuhkan)
- Calculate intersection (matched skills)
- Calculate gap (missing skills)
- Calculate match_score (% of JD skills yang dimiliki)

### 6. **Recommendation Generation** ✅
- File: `predictor.py` → `generate_recommendations()`
- Generate learning recommendations untuk setiap missing skill
- Format: "Pelajari dan tambahkan pengalaman terkait [skill] pada CV."

### 7. **Analysis Orchestration** ✅
- File: `predictor.py` → `analyze_cv()`
- Combine semua fitur di atas
- Return comprehensive analysis object dengan:
  - score, probability, isMatch
  - summary, matchedSkills, missingSkills, recommendedSkills

### 8. **Request Validation** ✅
- File: `schema.py`
- Pydantic model untuk request validation
- Support CV text, JD text, dan metadata fields (fullname, position, education, experience, skill)

### 9. **Test Files** ✅
- `test_predictor.py`: Testing predictor functions dengan 3 scenarios
- `test_predict.py`: Testing model inference dengan sample text

## Fitur yang Belum Selesai

### 1. **HTTP Endpoints** ❌ CRITICAL
- Status: Tidak ada endpoint yang didefinisikan
- App.py hanya loading model, belum ada route/endpoint
- Perlu endpoint untuk:
  - `POST /analyze` → accept AnalysisRequest → return analysis result
  - `GET /health` → health check
  - Mungkin `GET /skills` → return list of available skills

### 2. **Error Handling** ❌
- Tidak ada try-catch untuk model loading
- Tidak ada error handling untuk invalid inputs
- Tidak ada error handling untuk model inference failures

### 3. **Input Validation & Sanitization** ❌
- Schema hanya basic Pydantic validation
- Tidak ada length limits untuk cv_text dan job_description
- Tidak ada handling untuk very large inputs

### 4. **CORS Configuration** ❌
- Tidak ada CORS setup di FastAPI
- Diperlukan untuk backend Node.js dapat memanggil Python service

### 5. **Logging & Monitoring** ❌
- Tidak ada logging di aplikasi
- Tidak ada metrics untuk tracking inference performance

### 6. **API Documentation** ❌
- FastAPI auto-generate swagger docs, tapi endpoint belum ada
- Perlu dokumentasi untuk integration dengan Node.js backend

### 7. **Configuration Management** ❌
- Hardcoded paths (`model/skill_gap_model.keras`)
- Hardcoded threshold (0.45) di predictor.py
- Tidak ada environment variables atau config file

### 8. **Response Standardization** ❌
- Tidak ada standard response format/wrapper
- Tidak ada error response format

---

# AI MODULE

## Lokasi Model
**Path**: `model/skill_gap_model.keras`
**Format**: Keras H5 format (.keras)
**Size**: Tidak diketahui dari source code
**Architecture**: Neural network dengan custom SkillAttentionLayer

## Custom Layer yang Digunakan

### **SkillAttentionLayer**
**File**: `src/custom_layers.py`
**Fungsi**: Attention mechanism untuk TF-IDF features
**Cara Kerja**:
1. Input: TF-IDF vector (sparse → dense)
2. Attention weight computation: Dense(units=64, activation='tanh')
3. Softmax normalization: tf.nn.softmax(attention, axis=-1)
4. Output projection: Dense(units=64, activation='linear')
5. Return: projected_output * attention_weights

**Hyperparameters**:
- units: 64 (default, configurable)

**Purpose**: Belajar memberi bobot pada fitur TF-IDF yang relevan untuk prediksi matching

## Lokasi Vectorizer
**Path**: `model/tfidf_vectorizer.pkl`
**Type**: scikit-learn TF-IDF Vectorizer
**Format**: Pickle format (.pkl)
**Penggunaan**: 
- Transform raw text → sparse TF-IDF matrix
- Convert sparse → dense array dengan `.toarray()`
- Cast to float32 untuk TensorFlow compatibility

## Lokasi Skill Labels
**Path**: `model/skill_labels.json`
**Format**: JSON array
**Jumlah Skills**: 28 predefined skills
**Content**: ["agile", "aws", "communication", "css", "cyber security", "devops", "django", "docker", "ethical hacking", "flask", "git", "html", "jira", "linux", "marketing", "mongodb", "mysql", "nodejs", "penetration testing", "photoshop", "postgresql", "python", "react", "scrum", "seo", "sql", "ui", "ux"]

## Cara Model Di-load
**File**: `src/app.py`, `src/model_loader.py`

```python
model = tf.keras.models.load_model(
    "model/skill_gap_model.keras",
    custom_objects={
        "SkillAttentionLayer": SkillAttentionLayer
    },
    compile=False
)

vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

with open("model/skill_labels.json", "r") as f:
    skill_labels = json.load(f)
```

**Notes**:
- `compile=False`: Model tidak di-compile ulang, hanya untuk inference
- Custom objects perlu di-pass karena menggunakan custom layer
- Vectorizer di-load dengan joblib

## Cara Inference Berjalan

### Step-by-step Process:
1. **Input Preparation**:
   - Receive: cv_text, jd_text
   - Clean: gunakan `clean_text()` function
   - Combine: `cleaned_cv + " " + cleaned_jd`

2. **Vectorization**:
   - Transform combined text dengan vectorizer
   - Result: sparse matrix
   - Convert to dense: `.toarray()`
   - Cast to float32: `.astype("float32")`

3. **Model Prediction**:
   ```python
   probability = float(model.predict(vector, verbose=0)[0][0])
   ```
   - Input shape: (1, n_features) where n_features = vocabulary size
   - Output shape: (1, 1) → single probability value
   - Range: 0.0 to 1.0

4. **Classification**:
   - Compare dengan threshold (default: 0.45)
   - is_match = probability >= threshold
   - Score = probability * 100 (percentage)

## Input yang Dibutuhkan Model

### Format Input:
- **Type**: Sparse matrix (from vectorizer) → Dense array
- **Shape**: (1, n_features) where n_features depends on vectorizer vocabulary
- **dtype**: float32
- **Content**: TF-IDF weighted word frequencies dari combined CV+JD text

### Processing Pipeline:
1. Raw text (cv_text, jd_text)
2. → Clean text
3. → Combine
4. → Vectorize (sparse)
5. → Dense conversion
6. → float32 casting
7. → Model input

## Output yang Dihasilkan Model

### Direct Model Output:
- **Type**: NumPy array
- **Shape**: (1, 1)
- **Value**: Single float between 0 and 1
- **Meaning**: Probability that CV matches JD

### Processed Output dari `predict_match()`:
```python
{
    "match_probability": float (0-1),
    "is_match": boolean,
    "threshold": float,
    "score": float (0-100)
}
```

### Full Analysis Output dari `analyze_cv()`:
```python
{
    "score": float (0-100),
    "probability": float (0-1),
    "isMatch": boolean,
    "summary": string,
    "matchedSkills": list[str],
    "missingSkills": list[str],
    "recommendedSkills": list[str]
}
```

---

# BACKEND INTEGRATION STATUS

## Bagian yang Sudah Terintegrasi
- **Status**: TIDAK ADA yang terintegrasi dengan Node.js backend
- Core ML logic sudah siap, tapi belum expose via API

## Bagian yang Masih Mock
- **HTTP Endpoint**: Tidak ada endpoint, hanya file dengan logic
- **Integration**: Tidak ada

## Bagian yang Masih Perlu Dikerjakan

### CRITICAL (Harus dikerjakan sebelum integration):
1. **Buat HTTP Endpoint** 
   - Route: `POST /analyze`
   - Accept: AnalysisRequest (cv_text, job_description, optional metadata)
   - Return: Analysis result dengan standard response format
   - Error handling untuk invalid inputs

2. **Setup CORS**
   - Enable CORS middleware di FastAPI
   - Allow Node.js backend origin

3. **Error Handling & Response Standardization**
   - Wrap all responses dalam standard format: `{ success: bool, data: {}, error: string }`
   - Handle exceptions: model loading failures, invalid inputs, inference errors

### IMPORTANT (Sebelum production):
4. **Configuration Management**
   - Move hardcoded paths ke environment variables
   - Move threshold ke config (atau accept via request)

5. **Logging & Monitoring**
   - Add logging untuk track requests, inference time, errors
   - Add metrics untuk performance monitoring

6. **Input Validation**
   - Add length limits untuk cv_text dan job_description
   - Validate input types dan required fields

7. **Testing**
   - Integration test dengan Node.js backend
   - Load testing untuk model inference performance

### NICE TO HAVE:
8. Documentation
9. Rate limiting
10. Authentication/Authorization (if needed)
11. Caching (if applicable)

---

# DATA FLOW

## Complete Request-Response Cycle

### 1. Initial Request
```
Node.js Backend (HTTP POST)
    ↓
POST /analyze
Headers: Content-Type: application/json
Body: {
    "cv_text": "...",
    "job_description": "...",
    "fullname": "...",  (optional)
    "position": "...",  (optional)
    "education": "...", (optional)
    "experience": "...", (optional)
    "skill": "..." (optional)
}
```

### 2. FastAPI Request Processing
```
FastAPI Endpoint /analyze
    ↓
Pydantic Validation (AnalysisRequest)
    ↓ (if valid)
Call predictor.analyze_cv()
```

### 3. Predictor Processing
```
predictor.analyze_cv(cv_text, jd_text, model, vectorizer, skill_labels)
    │
    ├─→ predict_match()
    │   ├─→ clean_text(cv_text)
    │   ├─→ clean_text(jd_text)
    │   ├─→ Combine cleaned texts
    │   ├─→ vectorizer.transform() → sparse matrix
    │   ├─→ Convert to dense array (float32)
    │   ├─→ model.predict() → probability
    │   └─→ Return: {match_probability, is_match, threshold, score}
    │
    └─→ compute_skill_gap()
        ├─→ extract_cv_skills(cv_text, skill_labels)
        ├─→ extract_cv_skills(jd_text, skill_labels)
        ├─→ Calculate intersections (matched_skills)
        ├─→ Calculate difference (missing_skills)
        ├─→ Calculate match_score percentage
        └─→ Return: {cv_skills, jd_skills, matched_skills, missing_skills, match_score}
    
    ├─→ generate_recommendations(missing_skills)
    └─→ Return comprehensive analysis object
```

### 4. Response Generation
```
predictor.analyze_cv() returns:
{
    "score": 75.5,
    "probability": 0.755,
    "isMatch": true,
    "summary": "CV memiliki kecocokan 75.5% terhadap Job Description.",
    "matchedSkills": ["python", "sql", "aws", "docker"],
    "missingSkills": ["linux", "git"],
    "recommendedSkills": [
        "Pelajari dan tambahkan pengalaman terkait linux pada CV.",
        "Pelajari dan tambahkan pengalaman terkait git pada CV."
    ]
}
```

### 5. Final HTTP Response
```
FastAPI Response (HTTP 200 OK)
Headers: Content-Type: application/json
Body:
{
    "success": true,
    "data": {
        "score": 75.5,
        "probability": 0.755,
        "isMatch": true,
        "summary": "...",
        "matchedSkills": [...],
        "missingSkills": [...],
        "recommendedSkills": [...]
    }
}
```

## Data Transformation Details

### Text Cleaning Process
```
Raw Text:
"Python Developer with 3 years experience in Machine Learning and SQL.
Proficient in AWS, Docker, and Git."

↓ clean_text()

1. Lowercase:
"python developer with 3 years experience in machine learning and sql.
proficient in aws, docker, and git."

2. Remove URLs & emails:
(No change in this example)

3. Remove special characters (keep alphanumeric + space):
"python developer with 3 years experience in machine learning and sql
proficient in aws docker and git"

4. Normalize whitespace:
"python developer with 3 years experience in machine learning and sql proficient in aws docker and git"

Final Cleaned Text: All lowercase, no special chars, normalized spaces
```

### Vectorization Process
```
Cleaned Text:
"python developer with 3 years experience in machine learning and sql proficient in aws docker and git"

↓ vectorizer.transform()

Sparse Matrix (scipy.sparse):
Vocabulary indices untuk words yang ada di training set
Weights: TF-IDF scores

↓ .toarray()

Dense NumPy Array:
[[0.15, 0.0, 0.23, 0.0, ..., 0.18, 0.0, ...]]
(1D array dengan nilai TF-IDF untuk setiap vocab word)

↓ .astype("float32")

Model-compatible array format
```

### Model Inference
```
Dense float32 array (1, vocab_size)
↓
SkillAttentionLayer processes TF-IDF features
Learns attention weights untuk relevant features
↓
Dense output layer
↓
Sigmoid activation
↓
Single probability value (0-1)

Output: 0.755 (meaning 75.5% match)
```

---

# KNOWN ISSUES

## Code Issues Found

### 1. **No HTTP Endpoints Defined** ⚠️ CRITICAL
- **File**: `src/app.py`
- **Issue**: app.py hanya loading model, tidak ada route atau endpoint
- **Impact**: API tidak bisa diakses dari Node.js backend
- **Fix Required**: Tambahkan minimal 1 endpoint untuk `/analyze` POST request

### 2. **No Error Handling** ⚠️ HIGH
- **File**: `src/app.py`, `src/predictor.py`
- **Issues**:
  - Model loading tidak punya try-catch
  - Vectorizer loading tidak punya try-catch
  - No validation untuk cv_text dan job_description empty/null
  - No handling untuk vectorizer transform failure
  - No handling untuk model prediction failure
- **Impact**: Application crashes on error
- **Fix Required**: Add try-catch blocks dan proper error responses

### 3. **Hardcoded Paths** ⚠️ MEDIUM
- **File**: `src/app.py`, `src/model_loader.py`
- **Issue**: Model path hardcoded as `model/skill_gap_model.keras`
- **Impact**: 
  - Works only if app.py run from project root
  - Fails if run from different directory
  - Breaks if model files moved
- **Fix Required**: Use environment variables or config file + proper path resolution

### 4. **Hardcoded Threshold** ⚠️ MEDIUM
- **File**: `src/predictor.py`
- **Code**: `threshold = 0.45`
- **Issue**: Hardcoded, tidak flexible
- **Impact**: Cannot adjust sensitivity without code change
- **Fix Required**: Accept threshold dari request body atau environment variable

### 5. **Missing CORS Configuration** ⚠️ HIGH
- **File**: `src/app.py`
- **Issue**: No CORS middleware configured
- **Impact**: Node.js backend cannot call Python API (browser/CORS restrictions)
- **Fix Required**: Add `from fastapi.middleware.cors import CORSMiddleware`

### 6. **Duplicate Code** ⚠️ LOW
- **Files**: `src/app.py` and `src/model_loader.py` have identical model loading code
- **Impact**: Maintenance burden, inconsistency risk
- **Fix Required**: Centralize model loading logic

### 7. **Missing Input Validation** ⚠️ MEDIUM
- **File**: `src/schema.py`, endpoint (when created)
- **Issues**:
  - No max length validation for cv_text and job_description
  - No check for empty strings (just None)
  - No check for language (could be any language, model trained on specific language?)
- **Impact**: Potential DoS with very large inputs, unexpected model behavior
- **Fix Required**: Add validators in Pydantic model

### 8. **Potential Issue: Skill Extraction Greedy Matching** ⚠️ LOW
- **File**: `src/predictor.py` → `extract_cv_skills()`
- **Code**: `if skill.lower() in text`
- **Issue**: Substring matching, not word boundary
- **Example**: Text "docker" would match skill "docker", but also text "undocumented" might match something
- **Impact**: False positives in skill extraction
- **Note**: Depends on skill_labels content, but could be issue with skills like "sql" that appear in "mysql", "postgresql"
- **Fix Required**: Consider word tokenization or regex word boundaries

### 9. **No Logging** ⚠️ MEDIUM
- **Files**: All files
- **Issue**: No logging statements anywhere
- **Impact**: 
  - Cannot debug issues in production
  - Cannot track API usage
  - Cannot monitor inference performance
- **Fix Required**: Add logging module

### 10. **Missing Health Check** ⚠️ LOW
- **File**: `src/app.py`
- **Issue**: No health check endpoint
- **Impact**: Cannot verify if API is running and models are loaded correctly
- **Fix Required**: Add `GET /health` endpoint

### 11. **Type Hints Incomplete** ⚠️ LOW
- **Files**: `src/predictor.py`, `src/model_loader.py`
- **Issue**: Functions missing return type hints
- **Impact**: Less readable, harder to understand expected return types
- **Fix Required**: Add return type hints to all functions

### 12. **No Response Standardization** ⚠️ MEDIUM
- **Issue**: No standard response wrapper/format
- **Impact**: Client needs to know exact response structure, hard to add meta info (execution time, version, etc)
- **Fix Required**: Wrap all responses in standard format: `{ success: bool, data: {}, error?: string }`

---

# NEXT STEPS

## Checklist Prioritas Pekerjaan Berikutnya

### Phase 1: CRITICAL - Make API Functional 🔴
- [ ] **1.1** Create `POST /analyze` endpoint in `app.py`
  - Accept `AnalysisRequest`
  - Call `predictor.analyze_cv()`
  - Return analysis result
  - Priority: **CRITICAL** - blocks all backend integration
  
- [ ] **1.2** Create `GET /health` endpoint for health check
  - Verify model is loaded
  - Verify vectorizer is loaded
  - Return status
  - Priority: **HIGH** - needed for deployment verification

- [ ] **1.3** Add CORS middleware to FastAPI app
  - Enable Node.js backend origin
  - Priority: **CRITICAL** - blocks backend communication

- [ ] **1.4** Implement basic error handling
  - Try-catch for endpoint
  - Standard error response format
  - Log errors
  - Priority: **HIGH** - prevents API crashes

### Phase 2: IMPORTANT - Stabilize & Improve Quality 🟠
- [ ] **2.1** Add comprehensive input validation
  - Max length for cv_text, job_description
  - Validate non-empty
  - Sanitize inputs
  - Priority: **HIGH** - security & stability

- [ ] **2.2** Fix hardcoded paths
  - Use environment variables or config file
  - Use `os.path.join()` for cross-platform compatibility
  - Priority: **HIGH** - deployment issue

- [ ] **2.3** Make threshold configurable
  - Accept from request body (optional)
  - Fall back to environment variable
  - Fall back to default (0.45)
  - Priority: **MEDIUM** - feature flexibility

- [ ] **2.4** Remove duplicate code
  - Centralize model loading
  - Use shared function in app.py
  - Priority: **LOW** - maintenance

- [ ] **2.5** Add comprehensive logging
  - Log requests and responses
  - Log inference performance (duration)
  - Log errors with stack traces
  - Priority: **MEDIUM** - debugging & monitoring

### Phase 3: NICE TO HAVE - Polish & Optimization 🟡
- [ ] **3.1** Add type hints to all functions
  - Complete type hints
  - Priority: **LOW** - code quality

- [ ] **3.2** Standardize response format
  - Wrapper: `{ success: bool, data: {}, error?: string, meta?: {} }`
  - Priority: **MEDIUM** - API consistency

- [ ] **3.3** Optimize inference performance
  - Profile model inference time
  - Consider batch processing if needed
  - Priority: **LOW** - performance optimization

- [ ] **3.4** Add API documentation
  - FastAPI auto-docs (Swagger UI)
  - Document custom response format
  - Document error responses
  - Priority: **LOW** - documentation

- [ ] **3.5** Test with Node.js backend
  - Integration testing
  - End-to-end testing
  - Priority: **CRITICAL after Phase 1** - validation

- [ ] **3.6** Consider caching model predictions (if applicable)
  - Cache identical CV-JD pairs
  - Set TTL
  - Priority: **LOW** - optimization

### Phase 4: PRODUCTION - Pre-deployment Checklist ✅
- [ ] **4.1** Performance testing
  - Load test the endpoint
  - Profile memory usage
  - Profile inference latency
  
- [ ] **4.2** Security review
  - Input validation
  - No sensitive data in logs
  - Rate limiting consideration
  
- [ ] **4.3** Final integration testing with Node.js backend
  
- [ ] **4.4** Deployment documentation
  - Setup instructions
  - Environment variables needed
  - How to run with Uvicorn

- [ ] **4.5** Monitoring & alerting setup

## Execution Order

**Recommended immediate actions** (in order):
1. **1.1** Create `/analyze` endpoint (unblocks everything)
2. **1.3** Add CORS (unblocks backend communication)
3. **1.4** Add error handling (prevents crashes)
4. **1.2** Add `/health` endpoint (deployment check)
5. **2.1** Input validation (security)
6. **2.2** Fix hardcoded paths (deployment)
7. Test with backend

---

# IMPORTANT FILES

## File Importance & Function Matrix

| File | Importance | Function | Status | Notes |
|------|-----------|----------|--------|-------|
| `src/app.py` | 🔴 CRITICAL | FastAPI app entry point | ⚠️ Incomplete | Only loading models, no endpoints |
| `src/predictor.py` | 🔴 CRITICAL | Core ML logic | ✅ Complete | All functions implemented and tested |
| `src/custom_layers.py` | 🔴 CRITICAL | Custom attention layer | ✅ Complete | Required for model loading |
| `src/schema.py` | 🟠 HIGH | Request validation | ✅ Complete | Pydantic models for input |
| `model/skill_gap_model.keras` | 🔴 CRITICAL | Trained NN model | ✅ Ready | Core model for inference |
| `model/tfidf_vectorizer.pkl` | 🔴 CRITICAL | Text vectorizer | ✅ Ready | Transforms text to features |
| `model/skill_labels.json` | 🔴 CRITICAL | Skill taxonomy | ✅ Ready | 28 predefined skills |
| `src/model_loader.py` | 🟡 LOW | Standalone loader | ℹ️ Duplicate | Same code as app.py, can consolidate |
| `src/requirements.txt` | 🟠 HIGH | Dependencies | ✅ Complete | All packages listed |
| `src/test_predictor.py` | 🟡 LOW | Unit tests | ✅ Works | Tests predictor functions |
| `src/test_predict.py` | 🟡 LOW | Integration test | ✅ Works | Tests model inference |

## Critical Path Dependencies

```
app.py (entry point)
    ├─→ model/skill_gap_model.keras (model inference)
    ├─→ model/tfidf_vectorizer.pkl (text vectorization)
    ├─→ model/skill_labels.json (skill list)
    ├─→ custom_layers.py (SkillAttentionLayer for model loading)
    ├─→ predictor.py (analysis logic)
    │   ├─→ custom_layers.py (for model reference)
    │   └─→ All model/vectorizer artifacts
    └─→ schema.py (request validation)
```

---

# SUMMARY FOR FUTURE AI ASSISTANTS

## Quick Project Understanding

### What This Project Does
This is an **AI-powered CV-to-JD matching system** that:
1. Analyzes similarity between a Curriculum Vitae and a Job Description using a TensorFlow neural network
2. Identifies skill gaps (skills required by JD but missing from CV)
3. Generates personalized learning recommendations

### Technology Stack
- **Backend**: Python FastAPI + Uvicorn
- **ML**: TensorFlow/Keras (custom attention layer) + scikit-learn TF-IDF
- **Integration Target**: Node.js backend (not yet integrated)

### Current State
✅ **ML Logic**: Fully implemented and tested
❌ **API Endpoints**: Not created yet (BLOCKING ISSUE)
❌ **Integration**: Not started yet

### Key Components

**Model Architecture**:
- Input: TF-IDF vectorized combined CV+JD text
- Layer 1: Custom `SkillAttentionLayer` (attention mechanism on TF-IDF features)
- Output: Single probability (0-1) indicating match quality

**Analysis Pipeline**:
```
Raw CV + JD text
  ↓
Text cleaning (lowercase, remove special chars)
  ↓
Skill extraction (substring matching against 28 predefined skills)
  ↓
Model prediction (neural network inference)
  ↓
Skill gap analysis (intersection/difference of skill sets)
  ↓
Recommendation generation
```

### What's Working
- ✅ Model loading and inference
- ✅ Text cleaning and preprocessing
- ✅ Skill extraction from text
- ✅ Match probability prediction
- ✅ Skill gap analysis
- ✅ Recommendation generation
- ✅ Pydantic request validation

### What's NOT Working / Missing
- ❌ **HTTP endpoints** - app.py only loads models, no routes
- ❌ **CORS** - not configured for backend calls
- ❌ **Error handling** - no try-catch blocks
- ❌ **Input validation** - missing length limits
- ❌ **Configuration management** - hardcoded paths & threshold
- ❌ **Logging** - no logging anywhere
- ❌ **Documentation** - minimal

### Files to Know
1. **`src/app.py`** - Main entry point (need to add endpoints here)
2. **`src/predictor.py`** - All analysis logic (complete & working)
3. **`src/custom_layers.py`** - Custom Keras layer (required for model)
4. **`src/schema.py`** - Request validation models
5. **`model/skill_gap_model.keras`** - Trained neural network
6. **`model/tfidf_vectorizer.pkl`** - Text vectorizer
7. **`model/skill_labels.json`** - 28 predefined skills

### Immediate Next Steps
1. **Add endpoint**: Create `POST /analyze` in app.py that accepts AnalysisRequest and returns analysis result
2. **Add CORS**: Enable CORS middleware so Node.js backend can call it
3. **Error handling**: Add try-catch and proper error responses
4. **Test**: Verify endpoint works before Node.js integration

### How to Use (Currently)
```python
from predictor import analyze_cv
from model_loader import model, vectorizer, skill_labels

result = analyze_cv(cv_text, jd_text, model, vectorizer, skill_labels)
# result contains: score, probability, isMatch, matchedSkills, missingSkills, recommendations
```

### Integration Point with Backend
Node.js backend should call:
```
POST http://python-service:8000/analyze
Content-Type: application/json

{
  "cv_text": "...",
  "job_description": "...",
  "fullname": "..." (optional),
  "position": "..." (optional)
}
```

Response:
```json
{
  "success": true,
  "data": {
    "score": 75.5,
    "probability": 0.755,
    "isMatch": true,
    "summary": "CV memiliki kecocokan 75.5% terhadap Job Description.",
    "matchedSkills": ["python", "sql", "aws"],
    "missingSkills": ["linux", "git"],
    "recommendedSkills": ["Pelajari dan tambahkan pengalaman terkait linux pada CV.", ...]
  }
}
```

### Known Limitations
1. **Skill list is limited**: Only 28 predefined skills, substring matching (could match "mysql" as "sql")
2. **No language detection**: Model trained likely on English, behavior unknown for other languages
3. **Model threshold is hardcoded**: Cannot adjust sensitivity per request
4. **No batch processing**: Each request processed independently
5. **No caching**: Same CV-JD pairs processed multiple times

### Development Environment
- **Python version**: 3.x (likely 3.9+)
- **Package manager**: pip
- **Virtual environment**: `.venv/` folder exists
- **Test commands**: 
  - `python src/test_predictor.py` - test ML functions
  - `python src/test_predict.py` - test model inference

### Common Issues & Solutions
| Issue | Cause | Solution |
|-------|-------|----------|
| Model not found | Running from wrong directory | Use absolute paths or environment variables |
| SkillAttentionLayer not recognized | Custom layer not imported | Ensure `custom_objects={"SkillAttentionLayer": ...}` in load_model |
| CORS error from Node.js | No CORS middleware | Add FastAPI CORS middleware |
| Empty skill lists | Greedy substring matching | Consider word boundary matching instead |
| No response from API | No endpoints defined | Create endpoint routes in app.py |

---

## For Debugging

**If model doesn't load**:
- Check file paths exist: `model/skill_gap_model.keras`, `model/tfidf_vectorizer.pkl`, `model/skill_labels.json`
- Check `SkillAttentionLayer` is imported correctly
- Check TensorFlow version compatibility

**If predictions seem wrong**:
- Verify text cleaning is working: check output of `clean_text()`
- Verify vectorizer matches model training: check vocabulary size
- Check threshold value (currently 0.45)

**If backend cannot call API**:
- Ensure CORS middleware is added
- Verify FastAPI server is running on correct host/port
- Check network connectivity between Node.js and Python service

---

