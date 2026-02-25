import streamlit as st
import os
from utils.extractor import extract_text_from_bytes
from utils.processor import get_skills, get_jd_match
from utils.analyzer import predict_score, get_recommendations
from utils.report_gen import generate_pdf_report

# Page Config
st.set_page_config(page_title="Offline ML Resume Analyzer", layout="wide", page_icon="📄")

# App Styling & Effects
st.markdown("""
    <style>
    /* Main Background & Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Glassmorphism Effect for Cards */
    .stMetric, .stTabs, div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        padding: 20px !important;
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }

    /* Gradient Header */
    .hero-text {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    
    /* Button Hover Effects & Glass Focus */
    .stButton>button {
        border-radius: 10px;
        transition: all 0.3s ease;
        background: linear-gradient(90deg, #3b82f6, #1e3a8a);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
        transform: scale(1.05);
    }

    /* Glowing Metric Borders */
    div[data-testid="stMetric"] {
        border: 2px solid transparent !important;
        background-clip: padding-box, border-box !important;
        background-origin: padding-box, border-box !important;
        background-image: linear-gradient(to right, white, white), linear-gradient(90deg, #3b82f6, #8b5cf6) !important;
    }

    /* Confetti Container */
    #confetti-canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
    }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
""", unsafe_allow_html=True)

# Hero Section with Image Fallback
if os.path.exists('assets/resume_masterclass_banner.png'):
    st.image('assets/resume_masterclass_banner.png', use_column_width=True)
else:
    st.markdown('<div class="fade-in" style="background: linear-gradient(90deg, #1e3a8a, #3b82f6); height: 200px; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);"><h1 style="color: white; font-size: 3rem; font-weight: 800; text-shadow: 2px 2px 10px rgba(0,0,0,0.2);">Offline ML Resume Analyzer</h1></div>', unsafe_allow_html=True)

# Check if model exists
if not os.path.exists('models/ats_model.joblib'):
    st.error("🚩 ML Model not found! Please run `python train_model.py` first to initialize the system.")
    st.stop()

# Layout
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("📁 Upload Resume")
    uploaded_file = st.file_uploader("Choose PDF or DOCX format", type=["pdf", "docx"])
    
    st.markdown("---")
    st.subheader("🎯 Job Description (Optional)")
    jd_text = st.text_area("Paste the target job description to see matching keywords", height=200)

    if uploaded_file:
        raw_result = extract_text_from_bytes(uploaded_file)
        
        if isinstance(raw_result, dict) and "error" in raw_result:
            st.error(f"⚠️ {raw_result['error']}")
            st.stop()
            
        resume_text = raw_result
        
        if st.button("🚀 Analyze Resume", use_container_width=True):
            with st.spinner("Analyzing using Local ML Engine..."):
                # 1. Prediction
                score, err = predict_score(resume_text)
                if err:
                    st.error(err)
                else:
                    # 2. NLP Analysis
                    detected_skills = get_skills(resume_text)
                    match_percent, missing_keywords = get_jd_match(resume_text, jd_text)
                    recs = get_recommendations(score, missing_keywords)
                    
                    # 3. Victory Confetti
                    if score >= 80:
                        st.balloons()
                        st.markdown("""
                            <script>
                            confetti({
                                particleCount: 150,
                                spread: 70,
                                origin: { y: 0.6 },
                                colors: ['#3b82f6', '#1e3a8a', '#8b5cf6']
                            });
                            </script>
                        """, unsafe_allow_html=True)
                    
                    # Store in session state
                    st.session_state['analysis'] = {
                        'ats_score': score,
                        'detected_skills': detected_skills,
                        'match_percent': match_percent,
                        'missing_keywords': missing_keywords,
                        'recommendations': recs,
                        'resume_text': resume_text
                    }

with col2:
    st.subheader("📊 Analysis Dashboard")
    
    if 'analysis' in st.session_state:
        data = st.session_state['analysis']
        
        # Metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("ATS Score", f"{data['ats_score']}/100")
            st.progress(data['ats_score'] / 100)
        with m2:
            st.metric("Keyword Match", f"{data['match_percent']}%")
            st.progress(data['match_percent'] / 100)
            
        st.markdown("---")
        
        # Skills tabs
        tab1, tab2, tab3 = st.tabs(["✅ Detected Skills", "❌ Missing Keywords", "💡 Recommendations"])
        
        with tab1:
            if data['detected_skills']:
                st.write(", ".join(data['detected_skills']))
            else:
                st.info("No common tech skills detected in our local library.")
                
        with tab2:
            if data['missing_keywords']:
                st.error(", ".join(data['missing_keywords']))
            else:
                st.success("Great! No major skills missing relative to the JD.")
                
        with tab3:
            for r in data['recommendations']:
                st.write(f"- {r}")
                
        # Report Download
        st.markdown("---")
        report_data = {
            'ats_score': data['ats_score'],
            'detected_skills': data['detected_skills'],
            'missing_skills': data['missing_keywords'],
            'recommendations': data['recommendations']
        }
        
        try:
            pdf_bytes = generate_pdf_report(report_data)
            st.download_button(
                label="📥 Download Full PDF Analysis",
                data=pdf_bytes,
                file_name=f"Resume_Analysis_{st.session_state['analysis']['ats_score']}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.warning("Could not generate PDF report locally. Error: " + str(e))
            
    else:
        st.info("Upload a resume and click 'Analyze' to view insights.")
