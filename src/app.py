from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.schema import (AnalysisRequest, AnalyzeResponse, HealthResponse)
from src.predictor import analyze_cv
from src.model_loader import model, vectorizer, skill_labels

app = FastAPI(
    title="Hirely AI Service",
    version="1.0.0"
)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ganti nanti saat production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROOT

@app.get("/")
def root():
    return {
        "success": True,
        "service": "Hirely AI",
        "version": "1.0.0",
        "status": "running"
    }


# HEALTH CHECK

@app.get("/ping", response_model=HealthResponse)
def health_check():
    return {
        "success": True,
        "status": "healthy",
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "skill_count": len(skill_labels)
    }


# ANALYZE CV, INI ENDPOINT UTAMA KITA
# pake respon AnalyzeResponse
@app.post("/AIanalyses", response_model=AnalyzeResponse)
# param request nya ada di schema: AnalysisRequest
def analyze(request: AnalysisRequest):

    try:
        # kita panggil fungsi utama predictor, yaitu analyze_cv
        result = analyze_cv(
            cv_text=request.cv_text,
            jd_text=request.job_description,
            model=model,
            vectorizer=vectorizer,
            skill_labels=skill_labels
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )