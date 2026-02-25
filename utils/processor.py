import spacy
import json
import os
import streamlit as st

# Load skills dataset
try:
    with open('skills_dataset.json', 'r') as f:
        skills_data = json.load(f)
    ALL_SKILLS = skills_data['technical_skills'] + skills_data['soft_skills']
except:
    ALL_SKILLS = []

# Load spaCy
@st.cache_resource
def load_spacy_model():
    """Loads and caches the spaCy NLP model."""
    try:
        return spacy.load("en_core_web_sm")
    except:
        return None

nlp_engine = load_spacy_model()

@st.cache_data
def get_skills(text):
    """Extracts skills from text using local keyword matching and NLP."""
    if not text: return []
    text_lower = text.lower()
    found = []
    
    # Simple but effective keyword matching
    for skill in ALL_SKILLS:
        if f" {skill.lower()} " in f" {text_lower} " or text_lower.startswith(f"{skill.lower()} ") or text_lower.endswith(f" {skill.lower()}"):
            found.append(skill)
            
    return sorted(list(set(found)))

@st.cache_data
def get_jd_match(resume_text, jd_text):
    """Calculates match percentage and identifies missing keywords."""
    resume_skills = set(get_skills(resume_text))
    jd_skills = set(get_skills(jd_text))
    
    if not jd_skills:
        return 0, []
        
    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills
    match_percent = int((len(matched) / len(jd_skills)) * 100)
    
    return match_percent, sorted(list(missing))
