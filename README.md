# ATS Resume Checker Website

A Flask-based web application that analyzes resumes for Applicant Tracking System (ATS) compatibility and provides actionable feedback for improvement.

## Features

✅ **Resume Upload**: Support for PDF, DOCX, and TXT file formats  
✅ **ATS Score**: Get a comprehensive score out of 100  
✅ **Contact Information Extraction**: Automatically extracts email, phone, and LinkedIn profile  
✅ **Keyword Analysis**: Identifies technical skills, soft skills, certifications, and credentials  
✅ **Resume Statistics**: Word count and file size analysis  
✅ **Detailed Findings**: Get specific suggestions for improvement with severity levels  
✅ **Best Practices Guide**: Learn ATS dos and don'ts  
✅ **Responsive Design**: Works on desktop and mobile devices  

## Scoring Breakdown

The ATS score is calculated based on:

- **Keywords (40%)**: Technical skills, soft skills, certifications, and credentials
- **Format (30%)**: Proper formatting, section headers, bullet points, and structure
- **Content (30%)**: Quantifiable results, action verbs, and dates

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Click on the upload area or browse to select a resume file
3. The application will analyze your resume and display:
   - ATS Compatibility Score
   - Contact Information Found
   - Resume Statistics
   - Keywords Detected
   - Specific Suggestions for Improvement
4. Review the feedback and make improvements to your resume
5. Re-upload to check your progress

## ATS Best Practices

### ✓ Do's
- Use standard fonts (Arial, Calibri, Times New Roman)
- Use simple formatting and bullet points
- Include relevant keywords from job descriptions
- Use standard section headers (Experience, Education, Skills)
- Keep margins between 0.5 to 1 inch
- Save as PDF to preserve formatting
- Include quantifiable achievements and results
- Use clear, professional language

### ✗ Don'ts
- Avoid tables, columns, or text boxes
- Don't use images, graphics, or logos
- Avoid special characters and symbols
- Don't use headers, footers, or page breaks
- Avoid colored text or background
- Don't include personal photos
- Avoid abbreviations without explanation
- Don't use fancy formatting or unconventional fonts

## File Structure

```
.
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   └── home.html            # Main HTML template
└── static/
    ├── style.css            # Styling
    └── script.js            # Client-side functionality
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **File Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Icons**: Font Awesome

## Resume Analysis Features

### 1. Contact Information Extraction
- Email address
- Phone number
- LinkedIn profile

### 2. Keyword Detection
- Technical skills (Python, Java, SQL, React, etc.)
- Soft skills (Leadership, Communication, Teamwork, etc.)
- Certifications (AWS, Microsoft, Google, PMP, etc.)
- Educational credentials

### 3. Formatting Assessment
- File format compatibility
- Section structure
- Bullet point usage
- Presence of special characters

### 4. Content Quality
- Quantifiable results and metrics
- Action verbs (Developed, Implemented, Managed, etc.)
- Date information
- Word count optimization

### 5. Improvement Suggestions
Receives severity levels:
- **HIGH**: Critical issues affecting ATS compatibility
- **MEDIUM**: Important issues that should be addressed
- **LOW**: Minor suggestions for optimization

## Tips for Improving Your Score

1. **Add More Keywords**: Mirror keywords from the job posting into your resume
2. **Use Action Verbs**: Start bullet points with strong action verbs
3. **Include Metrics**: Quantify your achievements (percentages, numbers, timeframes)
4. **Optimize Length**: Aim for 250-500 words for optimal ATS parsing
5. **Standard Formatting**: Use simple fonts and layout without special formatting
6. **Clear Structure**: Use distinct section headers for Experience, Education, Skills
7. **Contact Info**: Make sure your email, phone, and LinkedIn are prominently displayed

## Limitations

- Maximum file size: 16MB
- Supported formats: PDF, DOCX, TXT
- Analysis is based on common ATS compatibility rules
- Results are suggestions and may vary by specific ATS systems

## Future Enhancements

- Job description comparison
- Skill gap analysis
- Multiple resume upload and comparison
- Resume template suggestions
- Export optimization report as PDF
- Integration with LinkedIn profile
- AI-powered content suggestions

## Troubleshooting

**Issue**: "Could not extract text from file"
- Ensure the PDF is not scanned image-based
- Try converting to DOCX or TXT format
- Check file is not corrupted

**Issue**: File upload not working
- Check file size (max 16MB)
- Verify file format is supported (PDF, DOCX, TXT)
- Ensure browser allows file upload

**Issue**: Port 5000 already in use
- Change port in app.py: `app.run(debug=True, port=5001)`

## Support

For issues or suggestions, please review your resume against the best practices guide and try again.

## License

This project is open source and available for personal and commercial use.

---

**Happy Resume Optimizing! 🎯**
