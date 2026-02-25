# 📄 Offline ML Resume Analyzer (No-API Version)

A professional, fully offline ATS resume analyzer powered by **Scikit-Learn**, **spaCy**, and **Streamlit**. No external AI APIs (like Gemini or OpenAI) are required.

## 🚀 Features
- **100% Offline**: Runs entirely on your local machine or private server.
- **Resume Validation**: 🛡️ Built-in heuristic check ensures only resumes are processed (not random PDFs).
- **ML-Based ATS Scoring**: Logistic Regression model for professional quality prediction.
- **Cloud Optimized**: Pre-configured for Streamlit Cloud with memory caching.
- **Multi-user Ready**: Safe, concurrent execution for public shared links.
- **PDF Reports**: Export results to a professional PDF instantly.

---

## 🛠️ Local Setup Instructions

1. **Clone/Setup the project:**
   ```bash
   mkdir offline-resume-analyzer && cd offline-resume-analyzer
   # (Copy the provided files into this directory)
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Initialize the ML Model:**
   *This step generates the synthetic data and trains the local model.*
   ```bash
   python train_model.py
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Streamlit Cloud Deployment Guide

1.  **GitHub**: Push your code to a GitHub repository.
2.  **Streamlit Cloud**:
    - Connect your repo.
    - Set the main file to `app.py`.
    - **Note**: The app will check for `models/ats_model.joblib`. If it's missing, ensure you've committed the `models/` folder after running `train_model.py` locally.

---

## 📁 Project Structure
- `app.py`: Main dashboard UI.
- `train_model.py`: Generates data and trains the Scikit-Learn model.
- `utils/`: Core utilities (Extraction, NLP, ML Inference, PDF Report).
- `models/`: Stores the trained `.joblib` model files.
- `skills_dataset.json`: The knowledge base for local skill detection.
