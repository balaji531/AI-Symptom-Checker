import json
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load dataset
with open("../data/diseases.json", "r", encoding="utf-8") as f:
    diseases = json.load(f)

texts = []
labels = []

for disease in diseases:
    disease_id = disease["id"]
    
    # English symptoms
    en_symptoms = disease["symptoms"]["en"]
    texts.append(" ".join(en_symptoms))
    labels.append(disease_id)

    # Tamil symptoms
    ta_symptoms = disease["symptoms"]["ta"]
    texts.append(" ".join(ta_symptoms))
    labels.append(disease_id)

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    ngram_range=(1,2),
    lowercase=True
)

X = vectorizer.fit_transform(texts)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, encoded_labels)

# Save files
joblib.dump(model, "model.joblib")
joblib.dump(vectorizer, "vec.joblib")
joblib.dump(label_encoder, "classes.joblib")

print("✅ Bilingual model trained successfully!")