import os
import json
import sqlite3
import time
import joblib

from flask import Flask, request, render_template, g, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change_this_secret")

# Allow React frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DATA_DIR, "audit.db")
DISEASE_KB = os.path.join(DATA_DIR, "diseases.json")

MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")
VECT_PATH = os.path.join(BASE_DIR, "vec.joblib")   # MUST match training file name
CLASSES_PATH = os.path.join(BASE_DIR, "classes.joblib")

# English + Tamil
LANG_MAP = {"en": "English", "ta": "Tamil"}

# ---------------- DATABASE ---------------- #

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS audits(
            id INTEGER PRIMARY KEY,
            timestamp INTEGER,
            input_text TEXT,
            lang TEXT,
            matched_symptoms TEXT,
            predictions TEXT
        )
    """)
    db.commit()


with app.app_context():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        open(DB_PATH, "a").close()
    init_db()

# ---------------- LOADERS ---------------- #

def load_kb():
    with open(DISEASE_KB, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model():
    model = joblib.load(MODEL_PATH)
    vect = joblib.load(VECT_PATH)
    label_encoder = joblib.load(CLASSES_PATH)
    return model, vect, label_encoder


# ---------------- SYMPTOM MATCHING ---------------- #

def match_symptoms_to_kb(symptom_text, kb, lang="en"):
    text = symptom_text.lower()
    found = set()

    for d in kb:
        for s in d.get("symptoms", {}).get(lang, []):
            if s.lower() in text:
                found.add(s)

    return list(found)


# ---------------- EMERGENCY RULE ---------------- #

def emergency_override(text):
    text = text.lower()

    emergency_keywords = [
        "chest pain",
        "shortness of breath",
        "confusion",
        "unconscious",
        "severe headache",
        "மார்பு வலி",
        "மூச்சுத்திணறல்",
        "குழப்பம்",
    ]

    for word in emergency_keywords:
        if word in text:
            return True

    return False


# ---------------- PREDICTION ENGINE ---------------- #

def predict_top_n(text, top_n=5):
    model, vect, label_encoder = load_model()
    kb = load_kb()

    X = vect.transform([text])
    probs = model.predict_proba(X)[0]

    class_ids = label_encoder.classes_

    class_probs = sorted(
        list(zip(class_ids, probs)),
        key=lambda x: -x[1]
    )[:top_n]

    predictions = []

    for cid, p in class_probs:
        ent = next((e for e in kb if e["id"] == cid), None)
        if not ent:
            continue

        predictions.append({
            "id": cid,
            "confidence": round(float(p) * 100, 2),
            "name_en": ent["name"].get("en", ""),
            "name_ta": ent["name"].get("ta", ""),
            "triage": ent.get("triage", "GP")
        })

    return predictions


# ---------------- WEB ROUTE ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    selected = "en"

    if request.method == "POST":
        text = request.form.get("symptoms", "").strip()
        lang = request.form.get("lang", "en")
        selected = lang if lang in LANG_MAP else "en"

        preds = predict_top_n(text)
        kb = load_kb()
        matched = match_symptoms_to_kb(text, kb, lang=selected)

        # Emergency override
        if emergency_override(text):
            preds.insert(0, {
                "id": "emergency_flag",
                "confidence": 100.0,
                "name_en": "Immediate Medical Attention Required",
                "name_ta": "உடனடி மருத்துவ கவனம் தேவை",
                "triage": "EMERGENCY"
            })

        db = get_db()
        db.execute(
            "INSERT INTO audits(timestamp,input_text,lang,matched_symptoms,predictions) VALUES (?,?,?,?,?)",
            (
                int(time.time()),
                text,
                selected,
                ",".join(matched),
                json.dumps(preds, ensure_ascii=False),
            ),
        )
        db.commit()

        result = {"predictions": preds, "matched": matched}

    return render_template(
        "index.html",
        result=result,
        langs=LANG_MAP,
        selected=selected
    )


# ---------------- API ROUTE ---------------- #

@app.route("/api/ask", methods=["POST"])
def api_ask():
    try:
        req = request.get_json()
        if not req:
            return jsonify({"error": "Invalid JSON"}), 400

        text = req.get("text", "").strip()
        lang = req.get("lang", "en")
        selected_lang = lang if lang in LANG_MAP else "en"

        if not text:
            return jsonify({"error": "Empty input"}), 400

        preds = predict_top_n(text)
        kb = load_kb()
        matched = match_symptoms_to_kb(text, kb, lang=selected_lang)

        if emergency_override(text):
            preds.insert(0, {
                "id": "emergency_flag",
                "confidence": 100.0,
                "name_en": "Immediate Medical Attention Required",
                "name_ta": "உடனடி மருத்துவ கவனம் தேவை",
                "triage": "EMERGENCY"
            })

        return jsonify({
            "predictions": preds,
            "matched": matched
        })

    except Exception as e:
        print("API ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)