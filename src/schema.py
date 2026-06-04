from pydantic import BaseModel
from typing import List

class AnalysisRequest(BaseModel):
    cv_text: str
    job_description: str
    fullname: str | None = None
    position: str | None = None
    education: str | None = None
    experience: str | None = None
    skill: str | None = None


class AnalysisResult(BaseModel):
    score: float
    isMatch: bool
    summary: str
    cv_skills: List[str]
    jd_skills: List[str]
    matchedSkills: List[str]
    missingSkills: List[str]
    recommendedSkills: List[str]


class AnalyzeResponse(BaseModel):
    success: bool
    data: AnalysisResult


class HealthResponse(BaseModel):
    success: bool
    status: str
    model_loaded: bool
    vectorizer_loaded: bool
    skill_count: int