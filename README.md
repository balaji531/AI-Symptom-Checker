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

- Load disease dataset (`diseases.json`)
- Extract symptoms in **English and Tamil**
- Convert symptoms to numeric vectors using **TF-IDF**
- Encode disease labels using **LabelEncoder**
- Train **Logistic Regression classifier**
- Save model using **Joblib**
- Flask loads the model and predicts diseases from user input

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

<img width="1102" height="648" alt="image" src="https://github.com/user-attachments/assets/40461909-f4f4-431b-91a9-f514e843226c" />

---

<img width="1128" height="956" alt="image" src="https://github.com/user-attachments/assets/d9f2fe05-e1d1-4d06-8270-176ef074bc4b" />

---

