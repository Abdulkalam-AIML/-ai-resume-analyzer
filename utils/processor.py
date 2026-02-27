import spacy
import json
import os
from functools import lru_cache

# Load skills dataset
@lru_cache(maxsize=1)
def load_skills():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(os.path.dirname(current_dir), 'skills_dataset.json')
        with open(file_path, 'r') as f:
            skills_data = json.load(f)
        return skills_data['technical_skills'] + skills_data['soft_skills']
    except:
        return []

# Load spaCy
@lru_cache(maxsize=1)
def load_spacy_model():
    """Loads and caches the spaCy NLP model."""
    try:
        # Try loading by name
        return spacy.load("en_core_web_sm")
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
        return None

nlp_engine = load_spacy_model()

def get_skills(text):
    """Extracts skills from text using local keyword matching and NLP."""
    if not text: return []
    skills_list = load_skills()
    text_lower = text.lower()
    found = []
    
    # Simple but effective keyword matching
    for skill in skills_list:
        if f" {skill.lower()} " in f" {text_lower} " or text_lower.startswith(f"{skill.lower()} ") or text_lower.endswith(f" {skill.lower()}"):
            found.append(skill)
            
    return sorted(list(set(found)))

def get_jd_match(resume_text, jd_text):
    """Calculates match percentage and identifies missing keywords."""
    resume_skills = set(get_skills(resume_text))
    jd_skills = set(get_skills(jd_text))
    
    if not jd_skills:
        return 0, []
        
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    match_percent = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0
    
    return match_percent, sorted(list(missing))
