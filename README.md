  # 🩺 AI Medical Symptom Checker

An AI-powered healthcare assistant that predicts possible diseases based on user symptoms using Machine Learning and Natural Language Processing.

---

# 📌 Overview

AI Medical Symptom Checker is a web-based intelligent health assistant that analyzes symptoms entered by users and predicts possible diseases with confidence scores.

The system uses **Natural Language Processing (NLP)** and **Machine Learning** to process symptoms in **English and Tamil**, making it accessible for a wider user base.

The application also includes **emergency symptom detection**, **triage recommendations**, and **audit logging** for tracking prediction history.

⚠ This tool provides informational guidance only and does not replace professional medical diagnosis.

---

# ✨ Key Features

- 🧠 Machine Learning–based disease prediction
- 🌐 Bilingual support (English & Tamil)
- ⚡ Fast symptom processing using TF-IDF
- 💾 SQLite audit logging of user queries
- 🔗 REST API for frontend integration
- 🖥 Web interface built using Flask

---

# 🛠 Tech Stack

| Layer               | Technology          |
| ------------------- | ------------------- |
| Frontend            | HTML, CSS           |
| Backend             | Python (Flask)      |
| Machine Learning    | Scikit-learn        |
| NLP                 | TF-IDF Vectorizer   |
| Model               | Logistic Regression |
| Data Storage        | JSON Dataset        |
| Logging             | SQLite              |
| Model Serialization | Joblib              |


---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/ai-symptom-checker.git
cd ai-symptom-checker
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Train the Machine Learning Model

```
cd backend
python train_model.py
```

This generates:

```
model.joblib
vec.joblib
classes.joblib
```

---

## 5️⃣ Run the Application

```
python app.py
```

Open browser:

```
http://localhost:5001
```

---

# 🧠 Machine Learning Pipeline

1️⃣ Load disease dataset (`diseases.json`)
2️⃣ Extract symptoms in **English and Tamil**
3️⃣ Convert symptoms to numeric vectors using **TF-IDF**
4️⃣ Encode disease labels using **LabelEncoder**
5️⃣ Train **Logistic Regression classifier**
6️⃣ Save model using **Joblib**
7️⃣ Flask loads the model and predicts diseases from user input

---

# 🚨 Emergency Detection

The system detects critical symptoms such as:

* Chest pain
* Shortness of breath
* Confusion
* Severe headache

If detected, the system immediately recommends **Emergency medical attention**.

---

# 📊 Example Input

```
fever cough shortness of breath
```

Example Output

| Disease   | Confidence |
| --------- | ---------- |
| COVID-19  | 88%        |
| Pneumonia | 74%        |
| Flu       | 62%        |

---

# 🔗 API Endpoint

POST request:

```
POST /api/ask
```

Example JSON request:

```
{
"text": "fever cough chest pain",
"lang": "en"
}
```

Example Response:

```
{
  "predictions":[...],
  "matched":[...]
}
```

---

# 🚀 Future Improvements

🔹 Deep Learning symptom classification
🔹 Larger medical dataset
🔹 Doctor recommendation system
🔹 Multi-language support
🔹 Mobile app integration
🔹 Integration with hospital APIs

---

# 👨‍💻 Author

Developed as an AI + Web Development project demonstrating the integration of Machine Learning, NLP, and Flask for healthcare assistance.
