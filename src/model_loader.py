import tensorflow as tf
import joblib
import json

from src.custom_layers import SkillAttentionLayer

# load model
model = tf.keras.models.load_model(
    "model/skill_gap_model.keras",
    custom_objects={"SkillAttentionLayer": SkillAttentionLayer},
    compile=False
)
print("\n\nModel load verified")

# load gatau apa namanya
with open("model/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = joblib.load(f)

# load label
with open("model/skill_labels.json", "r") as f:
    skill_labels = json.load(f)