from predictor import predict_match, compute_skill_gap
from model_loader import model, vectorizer, skill_labels

# CV Dummy
cv_text = """
Python developer with 3 years experience in machine learning and sql.
Proficient in aws, docker, and git. Strong communication skills.
"""
# Job Description Dummy
jd_text = """
We are looking for a Python developer with experience in sql and aws.
Knowledge of machine learning is a plus. Good communication required.
"""

cv_text1 = """
Photographer and graphic designer.
Expert in Photoshop and marketing.
"""
jd_text1 = """
Looking for Backend Developer.
Requirements:
- Python
- SQL
- Docker
- AWS
- Linux
"""

cv_text2 = """
Senior Backend Developer.
Python
SQL
AWS
Docker
Linux
Git
NodeJS
MongoDB
Communication
Agile
Scrum
"""
jd_text2 = """
Backend Developer.
Requirements:
Python
SQL
AWS
Docker
Linux
Git
Communication
"""

# Match Prediction
match_result = predict_match(
    cv_text,
    jd_text,
    model,
    vectorizer,
)
match_result1 = predict_match(
    cv_text1,
    jd_text1,
    model,
    vectorizer,
)
match_result2 = predict_match(
    cv_text2,
    jd_text2,
    model,
    vectorizer,
)

print("\n=== MATCH RESULT ===")
print("\n=== t1: umum ===")
for k, v in match_result.items():
    print(f"{k}: {v}")
print("\n=== t2: sangat ga cocok ===")
for k, v in match_result1.items():
    print(f"{k}: {v}")
print("\n=== t2: sangat cocok ===")
for k, v in match_result2.items():
    print(f"{k}: {v}")


# Skill Gap
gap_result = compute_skill_gap(
    cv_text,
    jd_text,
    skill_labels
)
gap_result1 = compute_skill_gap(
    cv_text1,
    jd_text1,
    skill_labels
)
gap_result2 = compute_skill_gap(
    cv_text2,
    jd_text2,
    skill_labels
)

print("\n=== SKILL GAP ===")
print("\n=== t1: umum ===")
for k, v in gap_result.items():
    print(f"{k}: {v}")
print("\n=== t2: sangat ga cocok ===")
for k, v in gap_result1.items():
    print(f"{k}: {v}")
print("\n=== t2: sangat cocok ===")
for k, v in gap_result2.items():
    print(f"{k}: {v}")