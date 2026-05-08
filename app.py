from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import PyPDF2
import re
from datetime import datetime
import json
import io
from docx import Document

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ATS Keywords Database
ATS_KEYWORDS = {
    'technical_skills': [
        'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'react', 'angular', 'vue',
        'node.js', 'django', 'flask', 'spring', 'mongodb', 'postgresql', 'mysql', 'aws', 'azure',
        'docker', 'kubernetes', 'git', 'api', 'rest', 'graphql', 'typescript', 'php', 'ruby',
        'golang', 'rust', 'machine learning', 'tensorflow', 'pytorch', 'data science', 'tableau',
        'power bi', 'excel', 'salesforce', '.net', 'ci/cd', 'jenkins', 'gitlab', 'github'
    ],
    'soft_skills': [
        'leadership', 'communication', 'team', 'collaboration', 'problem solving', 'critical thinking',
        'time management', 'organization', 'adaptability', 'motivation', 'creativity', 'analysis'
    ],
    'certifications': [
        'certification', 'certified', 'aws certified', 'microsoft certified', 'google certified',
        'pmp', 'scrum', 'agile', 'prince2', 'itil', 'cissp'
    ],
    'credentials': [
        'bachelor', 'master', 'phd', 'degree', 'diploma', 'associate', 'bs', 'ms', 'mba', 'university'
    ]
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text_from_txt(txt_path):
    text = ""
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
    return text

def extract_resume_text(file_path, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_type == 'docx':
        return extract_text_from_docx(file_path)
    elif file_type == 'txt':
        return extract_text_from_txt(file_path)
    return ""

def extract_contact_info(text):
    contact = {}
    
    # Email extraction
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, text)
    contact['email'] = email_match.group(0) if email_match else "Not found"
    
    # Phone extraction
    phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
    phone_match = re.search(phone_pattern, text)
    contact['phone'] = phone_match.group(0) if phone_match else "Not found"
    
    # LinkedIn extraction
    linkedin_pattern = r'linkedin\.com/in/[^\s]+'
    linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
    contact['linkedin'] = linkedin_match.group(0) if linkedin_match else "Not found"
    
    return contact

def calculate_ats_score(text):
    text_lower = text.lower()
    score = 0
    findings = []
    
    # 1. Keywords Score (40%)
    keyword_score = 0
    found_keywords = []
    
    for category, keywords in ATS_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                keyword_score += 1
                found_keywords.append(keyword)
    
    max_keywords = sum(len(keywords) for keywords in ATS_KEYWORDS.values())
    keyword_percentage = (keyword_score / max_keywords) * 40
    score += keyword_percentage
    
    if keyword_score < 10:
        findings.append({
            'issue': 'Low keyword count',
            'severity': 'high',
            'suggestion': f'Add relevant technical and soft skills keywords. Found {keyword_score} keywords.'
        })
    
    # 2. Format Score (30%)
    format_score = 30
    
    # Check for common formatting issues
    if '\t' in text or re.search(r'\.{2,}', text):
        format_score -= 5
        findings.append({
            'issue': 'Potential formatting issues',
            'severity': 'medium',
            'suggestion': 'Avoid excessive tabs, dots, or unusual formatting that may not parse correctly.'
        })
    
    # Check for bullet points
    if re.search(r'^[\s]*[•\-\*]\s', text, re.MULTILINE):
        format_score += 5
    
    # Check for clear sections
    sections = ['experience', 'education', 'skills', 'summary', 'objective']
    found_sections = sum(1 for section in sections if section in text_lower)
    section_score = (found_sections / len(sections)) * 10
    format_score = max(30 - 5, min(format_score + section_score, 30))
    
    score += format_score
    
    # 3. Content Score (30%)
    content_score = 0
    
    # Check for quantifiable results
    numbers = re.findall(r'\d+%|\d+\s*(?:million|billion|thousand|k|m)', text)
    if numbers:
        content_score += 10
    else:
        findings.append({
            'issue': 'Lack of quantifiable results',
            'severity': 'medium',
            'suggestion': 'Include metrics and numbers (e.g., "increased sales by 20%", "managed team of 5").'
        })
    
    # Check for action verbs
    action_verbs = ['developed', 'implemented', 'designed', 'managed', 'led', 'created', 'improved',
                    'achieved', 'increased', 'reduced', 'optimized', 'coordinated', 'collaborated']
    action_verb_count = sum(1 for verb in action_verbs if verb in text_lower)
    
    if action_verb_count < 3:
        findings.append({
            'issue': 'Few action verbs',
            'severity': 'low',
            'suggestion': f'Use more action verbs to describe achievements. Currently found {action_verb_count}.'
        })
        content_score += 10
    else:
        content_score += 15
    
    # Check for dates
    date_pattern = r'\b(19|20)\d{2}\b|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    if re.search(date_pattern, text):
        content_score += 5
    else:
        findings.append({
            'issue': 'Missing or unclear dates',
            'severity': 'low',
            'suggestion': 'Include clear dates for your work experience and education.'
        })
    
    score += content_score
    
    # 4. Length Check
    word_count = len(text.split())
    if word_count < 250:
        findings.append({
            'issue': 'Resume too short',
            'severity': 'high',
            'suggestion': f'Current length: {word_count} words. Aim for 250-500 words.'
        })
    elif word_count > 1000:
        findings.append({
            'issue': 'Resume too long',
            'severity': 'medium',
            'suggestion': f'Current length: {word_count} words. Keep it to 500-1000 words for better ATS parsing.'
        })
    
    # 5. Character encoding issues
    if len([c for c in text if ord(c) > 127]) > len(text) * 0.1:
        findings.append({
            'issue': 'Special characters detected',
            'severity': 'low',
            'suggestion': 'Use standard ASCII characters. Some special symbols may not parse correctly in ATS.'
        })
    
    return round(score, 2), findings, found_keywords, word_count

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX, TXT'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Extract file type
        file_type = filename.rsplit('.', 1)[1].lower()
        
        # Extract text from resume
        resume_text = extract_resume_text(filepath, file_type)
        
        if not resume_text:
            return jsonify({'error': 'Could not extract text from file'}), 400
        
        # Extract contact information
        contact_info = extract_contact_info(resume_text)
        
        # Calculate ATS score
        ats_score, findings, keywords, word_count = calculate_ats_score(resume_text)
        
        # Prepare response
        result = {
            'success': True,
            'ats_score': ats_score,
            'contact_info': contact_info,
            'findings': findings,
            'keywords_found': list(set(keywords))[:20],  # Top 20 unique keywords
            'word_count': word_count,
            'file_size': os.path.getsize(filepath),
            'filename': filename
        }
        
        # Clean up file
        os.remove(filepath)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ats-tips')
def get_ats_tips():
    tips = {
        'dos': [
            'Use standard fonts (Arial, Calibri, Times New Roman)',
            'Use simple formatting and bullet points',
            'Include relevant keywords from job description',
            'Use standard section headers (Experience, Education, Skills)',
            'Keep margins between 0.5 to 1 inch',
            'Save as PDF to preserve formatting',
            'Use simple date formats (MM/YY or MM/DD/YYYY)',
            'Include quantifiable achievements and results'
        ],
        'donts': [
            'Avoid tables, columns, or text boxes',
            'Don\'t use images, graphics, or logos',
            'Avoid special characters and symbols',
            'Don\'t use headers, footers, or page breaks',
            'Avoid colored text or background',
            'Don\'t include personal photos',
            'Avoid abbreviations without explanation',
            'Don\'t use fancy formatting or unconventional fonts'
        ],
        'keywords': [
            'Technical skills: Programming languages, tools, frameworks',
            'Soft skills: Leadership, communication, teamwork',
            'Certifications: Relevant industry certifications',
            'Education: Degrees and institutions',
            'Results: Percentages, metrics, achievements'
        ]
    }
    return jsonify(tips)

if __name__ == '__main__':
    app.run(debug=True)