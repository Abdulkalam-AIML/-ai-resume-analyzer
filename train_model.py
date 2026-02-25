import pandas as pd
import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# 1. Generate Synthetic Dataset
def generate_synthetic_data():
    resumes = [
        "Experienced Python Developer with expertise in Django, Flask, and PostgreSQL. Worked on scalable web apps.",
        "Data Scientist skilled in Machine Learning, Pandas, NumPy, and Scikit-Learn. Passionate about AI.",
        "Frontend React Developer with experience in HTML, CSS, JavaScript, and UI design.",
        "Junior Developer with basic knowledge of C++, Java and basic HTML.",
        "Senior DevOps Engineer specializing in AWS, Docker, Kubernetes and CI/CD pipelines.",
        "HR Manager with 10 years of experience in recruitment, teamwork and leadership.",
        "Project Manager with Agile and Scrum certifications. Excellent communication skills.",
        "Software Engineer with Java, Spring Boot and AWS experience. Built microservices.",
        "Intern with limited experience in Excel and basic Python scripting.",
        "Full Stack Developer proficient in React, Node.js, and MongoDB."
    ]
    # Synthetic ATS scores (randomized for illustration but logically mapped)
    scores = [85, 90, 80, 40, 95, 75, 88, 92, 30, 87]
    
    # Map scores to categories for Logistic Regression (e.g., Low, Medium, High)
    # We'll use 0: Low (<50), 1: Med (50-80), 2: High (>80)
    labels = [2 if s > 80 else 1 if s >= 50 else 0 for s in scores]
    
    return pd.DataFrame({'text': resumes, 'label': labels, 'score': scores})

# 2. Train Model
def train_and_save():
    df = generate_synthetic_data()
    
    # Vectorization
    tfidf = TfidfVectorizer(stop_words='english', max_features=500)
    X = tfidf.fit_transform(df['text'])
    y = df['label']
    
    # Model Training
    model = LogisticRegression()
    model.fit(X, y)
    
    # Save Model and Vectorizer
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/ats_model.joblib')
    joblib.dump(tfidf, 'models/tfidf_vectorizer.joblib')
    print("✅ Model and Vectorizer saved to 'models/'")

if __name__ == "__main__":
    train_and_save()
