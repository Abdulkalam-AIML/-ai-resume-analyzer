from flask import Flask
from flask_cors import CORS
import os
import io

# We need a custom template folder because we are in api/ subdirectory
app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Lazy loading models in routes instead of at boot

@app.route('/')
def index():
    from flask import render_template
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    from flask import request, jsonify
    from utils.extractor import extract_text_from_bytes
    from utils.processor import get_skills, get_jd_match
    from utils.analyzer import predict_score, get_recommendations
    
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    
    file = request.files['resume']
    jd_text = request.form.get('jd', '')
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        file_bytes = file.read()
        # In-memory file-like object for extractor
        file_io = io.BytesIO(file_bytes)
        
        # We need to pass both the stream and the filename to determine extension
        resume_text = extract_text_from_bytes(file_io, file.filename)
        
        if isinstance(resume_text, dict) and "error" in resume_text:
            return jsonify({"error": resume_text['error']}), 400
        
        # 1. Prediction
        score, err = predict_score(resume_text)
        if err:
            return jsonify({"error": err}), 500
            
        # 2. NLP Analysis
        detected_skills = get_skills(resume_text)
        match_percent, missing_keywords = get_jd_match(resume_text, jd_text)
        recs = get_recommendations(score, missing_keywords)
        
        return jsonify({
            'ats_score': score,
            'detected_skills': list(detected_skills),
            'match_percent': match_percent,
            'missing_keywords': list(missing_keywords),
            'recommendations': recs,
            'resume_text': resume_text[:500] + "..." # Truncate for safety
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-report', methods=['POST'])
def generate_report():
    from flask import request, jsonify, send_file
    from utils.report_gen import generate_pdf_report
    data = request.json
    try:
        pdf_bytes = generate_pdf_report(data)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Resume_Analysis_{data.get('ats_score', 0)}.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
