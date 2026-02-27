# 📄 Offline ML Resume Analyzer

A professional, fully offline ATS resume analyzer powered by **Flask**, **Scikit-Learn**, and **spaCy**. Features a premium, modern UI with 100% local processing.

## 🚀 Key Features

- **100% Offline**: Runs entirely on your local machine. No external APIs (Gemini/OpenAI) required.
- **Privacy First**: Your resumes never leave your system.
- **ML-Based Scoring**: Predicts ATS quality using a local Logistic Regression model.
- **Professional Reports**: One-click PDF export for analysis results.
- **Cross-Platform**: Designed to run on Windows, macOS, and Linux.

---

## 🛠️ Setup & Execution (All Systems)

### 1. Prerequisites
Ensure you have **Python 3.9+** installed.

### 2. Install Dependencies
Open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux) and run:
```bash
pip install -r requirements.txt
```

### 3. Initialize the ML Model
Before running the app for the first time, you must train the local model:
```bash
python train_model.py
```
*This generates the synthetic training data and saves the model to the `models/` folder.*

### 4. Launch the Application
Run the Flask server:
```bash
python main.py
```
After the server starts, open your browser and navigate to:
**[http://127.0.0.1:5001](http://127.0.0.1:5001)**

---

## 📁 Project Structure

- `main.py`: Flask web server and API.
- `train_model.py`: Model training script.
- `static/`: Frontend assets (CSS, JS).
- `templates/`: HTML interface.
- `utils/`: Core logic (Extraction, NLP, ML, PDF Reports).
- `models/`: Trained model storage.

---

## ☁️ Deployment (Vercel)

This project is pre-configured for Vercel. 
1. Push your code to a GitHub repository.
2. Link the repository to your Vercel account.
3. Vercel will automatically detect the configuration and deploy the Flask app.

> [!NOTE]
> The app is configured to run on port **5001** locally to avoid common system conflicts on macOS. On Vercel, it will automatically use the standard web port.
