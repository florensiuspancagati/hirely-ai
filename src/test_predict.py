import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import joblib

from custom_layers import SkillAttentionLayer

model = tf.keras.models.load_model(
    "model/skill_gap_model.keras",
    custom_objects={
        "SkillAttentionLayer": SkillAttentionLayer
    },
    compile=False
)

vectorizer = joblib.load("model/tfidf_vectorizer.pkl")

sample_text = """
React NodeJS MongoDB Express REST API Docker Git
"""

# TF-IDF
x = vectorizer.transform([sample_text])

# Sparse -> Dense
x = x.toarray().astype("float32")

print("\n\nInput shape:", x.shape)

prediction = model.predict(x, verbose=0)

print("Prediction:")
print(prediction)

print("Prediction shape:")
print(prediction.shape)

print("Match score:")
print(float(prediction[0][0]))