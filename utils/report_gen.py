from fpdf import FPDF
import datetime

class ResumeReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'AI Resume Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(data):
    """
    Generates a professional PDF report.
    data: dict containing ats_score, skills, missing_skills, recommendations
    """
    pdf = ResumeReport()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)

    # Date
    pdf.cell(0, 10, f"Date: {datetime.date.today().strftime('%B %d, %Y')}", 0, 1)
    pdf.ln(5)

    # ATS Score
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 10, f"ATS Score: {data['ats_score']}/100", 0, 1)
    pdf.ln(5)

    # Detected Skills
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 10, "Detected Skills:", 0, 1)
    pdf.set_font("helvetica", size=11)
    skills_text = ", ".join(data['detected_skills'])
    pdf.multi_cell(0, 10, skills_text)
    pdf.ln(5)

    # Missing Skills
    if data.get('missing_skills'):
        pdf.set_font("helvetica", 'B', 12)
        pdf.cell(0, 10, "Missing Key Skills (Match vs JD):", 0, 1)
        pdf.set_font("helvetica", size=11)
        missing_text = ", ".join(data['missing_skills'])
        pdf.multi_cell(0, 10, missing_text)
        pdf.ln(5)

    # Recommendations
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(0, 10, "Recommendations:", 0, 1)
    pdf.set_font("helvetica", size=11)
    for rec in data['recommendations']:
        pdf.multi_cell(0, 10, f"- {rec}")

    return pdf.output()
