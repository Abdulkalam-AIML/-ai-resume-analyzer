import joblib
from functools import lru_cache

@lru_cache(maxsize=1)
def load_ml_models():
    """Loads and caches the ML model and vectorizer for performance."""
    try:
        model = joblib.load('models/ats_model.joblib')
        vectorizer = joblib.load('models/tfidf_vectorizer.joblib')
        return model, vectorizer, ""
    except Exception as e:
        return None, None, f"Models initialization error: {str(e)}"

def predict_score(text):
    """Predicts a 0-100 score using the offline ML model."""
    model, vectorizer, err = load_ml_models()
    if err:
        return 0, err
    
    # Vectorize and Predict Category
    X = vectorizer.transform([text])
    category = model.predict(X)[0] # 0: Low, 1: Med, 2: High
    
    # Map category to a score range for UI
    if category == 2:
        base_score = 85
    elif category == 1:
        base_score = 60
    else:
        base_score = 30
        
    # Add some variance based on text length and skill density
    variance = min(len(text.split()) / 50, 10) # Max 10 bonus points
    final_score = min(int(base_score + variance), 100)
    
    return final_score, ""

def get_recommendations(score, missing_skills):
    """Generates offline recommendations based on score and missing skills."""
    recs = []
    if score < 50:
        recs.append("Critical: Improve your resume structure and add more technical keywords.")
    elif score < 80:
        recs.append("Good: Consider quantifying your achievements with metrics.")
    
    if missing_skills:
        recs.append(f"Missing Key Skills: {', '.join(missing_skills[:5])}")
    
    recs.append("Ensure your contact information is clearly visible.")
    recs.append("Use bullet points for better readability.")
    
    return recs
