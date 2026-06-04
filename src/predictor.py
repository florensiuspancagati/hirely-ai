import re

threshold = 0.45

# FUNGSI UNTUK CLEANING TEKS
def clean_text(text: str) -> str:
  if not isinstance(text, str) or not text.strip(): return ""
  text = text.lower()
  text = re.sub(r"http\S+|www\S+", " ", text)
  text = re.sub(r"\S+@\S+", " ", text)
  text = re.sub(r"[^a-z0-9\s]", " ", text)
  text = re.sub(r"\s+", " ", text).strip()
  return text

# EKSTRAK SKILL DI CV
def extract_cv_skills(cv_text: str, skill_labels: list) -> list:
  text = cv_text.lower()
  return sorted([skill for skill in skill_labels if skill.lower() in text])

# FUNGSI UNTUK PREDIKSI KECOCOKAN CV DENGAN JD
def predict_match(cv_text: str, jd_text: str, model, vectorizer, threshold: float = 0.5) -> dict:
  combined_text = clean_text(cv_text) + " " + clean_text(jd_text)
  vector = vectorizer.transform([combined_text]).toarray().astype("float32")
  probability = float(model.predict(vector, verbose=0)[0][0])
  is_match = probability >= threshold
  score = round(probability * 100, 2)

  return {
      "match_probability": round(probability, 4),
      "is_match": bool(is_match),
      "threshold": threshold,
      "score": score,
  }

# FUNGSI UNTUK MENCARI GAP SKILL
def compute_skill_gap(cv_text: str, jd_text: str, skill_labels: list) :
  cv_skills = set(extract_cv_skills(cv_text, skill_labels))
  jd_skills = set(extract_cv_skills(jd_text, skill_labels))
  matched_skills = cv_skills & jd_skills
  gap_skills = jd_skills - cv_skills
  match_score = round(len(matched_skills)/len(jd_skills) * 100, 1) if jd_skills else 0.0

  return {
    "cv_skills": sorted(cv_skills),
    "jd_skills": sorted(jd_skills),
    "matched_skills": sorted(matched_skills),
    "missing_skills": sorted(gap_skills),
    "match_score": match_score,
  }


def generate_recommendations(missing_skills):
  recommendations = []

  for skill in missing_skills:
      recommendations.append(
          f"Pelajari dan tambahkan pengalaman terkait {skill} pada CV."
      )

  return recommendations


def analyze_cv(
  cv_text,
  jd_text,
  model,
  vectorizer,
  skill_labels,
):
  match_result = predict_match(
      cv_text,
      jd_text,
      model,
      vectorizer,
  )

  gap_result = compute_skill_gap(
      cv_text,
      jd_text,
      skill_labels,
  )

  summary = (
      f"CV memiliki kecocokan "
      f"{match_result['score']}% "
      f"terhadap Job Description."
  )

  return {
      "score": match_result["score"],
      "isMatch": match_result["is_match"],
      "summary": summary,
      "cv_skills": gap_result["cv_skills"],
      "jd_skills": gap_result["jd_skills"],
      "matchedSkills": gap_result["matched_skills"],
      "missingSkills": gap_result["missing_skills"],
      "recommendedSkills": generate_recommendations(gap_result["missing_skills"]),
  }