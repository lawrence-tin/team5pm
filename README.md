# 🎬 MrBeast Performance Intelligence Platform (Team5PM)

An end-to-end **data engineering + machine learning + analytics platform** that ingests YouTube data, transforms it in Snowflake, and provides an interactive Streamlit dashboard to predict video performance.

Built as a production-style pipeline using modern data stack tools: **Python, Snowflake, Streamlit, GitHub Actions, and Machine Learning (scikit-learn)**.

---

## 🚀 Live Demo
[https://team5pmlawrence.streamlit.app/]

---

## 📌 Project Overview

This project simulates a real-world **content performance intelligence system** inspired by YouTube analytics workflows used in media companies.

It covers:

- API ingestion (YouTube Data API)
- Bronze → Silver → Gold data architecture in Snowflake
- Feature engineering for ML modeling
- Machine learning prediction of engagement rates
- Interactive analytics dashboard in Streamlit
- CI/CD-ready ingestion pipeline (GitHub Actions ready)

---

## 🏗️ Architecture


YouTube API
↓
Bronze Layer (Raw JSON in Snowflake)
↓
Silver Layer (Cleaned & structured data)
↓
Gold Layer (ML-ready dataset)
↓
Streamlit Dashboard (Analytics + Predictions)


---

## 📊 Key Features

### 📡 Data Engineering
- YouTube API ingestion for MrBeast channel videos
- NDJSON raw ingestion format
- Snowflake staging + COPY INTO pipeline
- Structured Bronze → Silver → Gold transformation layers

### 🤖 Machine Learning
- Engagement rate prediction model
- Feature engineering:
  - Title length
  - Posting hour
  - Duration
  - Engagement history rolling averages
- Scikit-learn trained regression model
- Serialized using `joblib`

### 📈 Analytics Dashboard (Streamlit)
- KPI overview (views, engagement, top videos)
- Time series trends
- Duration vs performance analysis
- Top-performing videos table
- Interactive ML prediction tool

### ☁️ Cloud & Deployment
- Snowflake data warehouse integration
- Streamlit Cloud deployment ready
- GitHub Actions-ready ingestion pipeline

---

## 🧠 Machine Learning Model

**Target:** Engagement Rate (%)  
**Model Type:** Regression model (scikit-learn)

### Input Features:
- Video duration
- Title complexity
- Posting hour
- Weekend flag
- Historical rolling averages (views, engagement, duration)

---

## 📂 Project Structure


team5pm-streamlit-app/
│
├── streamlit_app.py # Main Streamlit dashboard
├── ingestion_bronze.py # YouTube API → Snowflake pipeline
├── requirements.txt
├── README.md
│
├── .streamlit/
│ └── secrets.toml # Snowflake credentials (NOT committed)
│
├── models/
│ └── engagement_model.joblib.gz
│
├── utils/
│ ├── data_loader.py # Snowflake queries
│ ├── features.py # Feature engineering
│ └── prediction.py # ML model loading
│
└── assets/
└── mrbeast.jpg


---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/lawrence-tin/team5pm-streamlit-app.git
cd team5pm-streamlit-app
2. Install Dependencies
pip install -r requirements.txt
3. Configure Secrets (Streamlit Cloud or Local)

Create file:

.streamlit/secrets.toml

Example:

[snowflake]
user = "your_user"
password = "your_password"
account = "your_account"
warehouse = "your_warehouse"
database = "your_database"
schema = "your_schema"
role = "your_role"
4. Run Streamlit App
streamlit run streamlit_app.py
🔁 Data Ingestion Pipeline

Run manually:

python ingestion_bronze.py
What it does:
Fetches latest MrBeast videos via YouTube API
Converts response into NDJSON format
Uploads raw JSON to Snowflake Bronze table
Loads structured data via COPY INTO
⚡ Future Improvements
Automate ingestion via GitHub Actions (scheduled runs)
Add Airflow orchestration
Improve ML model (XGBoost / LightGBM)
Add real-time streaming ingestion
Add user authentication to dashboard
Deploy full stack on AWS + Snowflake hybrid
👨‍💻 Author

Lawrence Tinago
Data Engineer | Data Scientist
Specializing in Snowflake, Azure, AWS, and ML pipelines

📜 License

This project is for educational and portfolio purposes.


---
