// DOM Elements
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const resultsSection = document.getElementById('resultsSection');
const loadingState = document.getElementById('loadingState');
const newCheckBtn = document.getElementById('newCheckBtn');
const uploadArea = document.querySelector('.upload-area');

// File Input Handlers
browseBtn.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and Drop Handlers
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// New Check Button
newCheckBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    uploadArea.style.display = 'block';
    fileInput.value = '';
});

// File Handler
function handleFile(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain'];
    const allowedExtensions = ['.pdf', '.docx', '.txt'];
    
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedExtensions.includes(fileExt) && !allowedTypes.includes(file.type)) {
        alert('Please upload a PDF, DOCX, or TXT file');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        alert('File size exceeds 16MB limit');
        return;
    }
    
    uploadResume(file);
}

// Upload Resume
function uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading state
    uploadArea.style.display = 'none';
    loadingState.style.display = 'block';
    resultsSection.style.display = 'none';
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayResults(data);
            loadingState.style.display = 'none';
            resultsSection.style.display = 'block';
        } else {
            alert('Error: ' + data.error);
            loadingState.style.display = 'none';
            uploadArea.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing your resume');
        loadingState.style.display = 'none';
        uploadArea.style.display = 'block';
    });
}

// Display Results
function displayResults(data) {
    const score = data.ats_score;
    
    // Update Score Circle
    const scoreProgress = document.getElementById('scoreProgress');
    const scoreValue = document.getElementById('scoreValue');
    const scoreRating = document.getElementById('scoreRating');
    
    scoreValue.textContent = Math.round(score);
    
    // Calculate stroke dashoffset for progress circle
    const strokeDashoffset = 565 * (1 - score / 100);
    scoreProgress.style.strokeDashoffset = strokeDashoffset;
    
    // Update score color based on rating
    if (score >= 80) {
        scoreProgress.style.stroke = '#10b981';
        scoreRating.className = 'score-rating rating-excellent';
        scoreRating.textContent = 'Excellent! Your resume is ATS-friendly';
    } else if (score >= 60) {
        scoreProgress.style.stroke = '#10b981';
        scoreRating.className = 'score-rating rating-good';
        scoreRating.textContent = 'Good! Your resume passes ATS checks';
    } else if (score >= 40) {
        scoreProgress.style.stroke = '#f59e0b';
        scoreRating.className = 'score-rating rating-fair';
        scoreRating.textContent = 'Fair. Consider the suggestions below';
    } else {
        scoreProgress.style.stroke = '#ef4444';
        scoreRating.className = 'score-rating rating-poor';
        scoreRating.textContent = 'Needs Improvement. Review suggestions';
    }
    
    // Display Contact Info
    displayContactInfo(data.contact_info);
    
    // Display Stats
    displayStats(data.word_count, data.file_size);
    
    // Display Keywords
    displayKeywords(data.keywords_found);
    
    // Display Findings
    displayFindings(data.findings);
}

// Display Contact Info
function displayContactInfo(contact) {
    const contactInfo = document.getElementById('contactInfo');
    contactInfo.innerHTML = '';
    
    const fields = [
        { label: 'Email', value: contact.email },
        { label: 'Phone', value: contact.phone },
        { label: 'LinkedIn', value: contact.linkedin }
    ];
    
    fields.forEach(field => {
        const div = document.createElement('div');
        div.className = 'contact-item' + (field.value === 'Not found' ? ' not-found' : '');
        
        if (field.value !== 'Not found') {
            div.innerHTML = `<strong>${field.label}:</strong> <span>${field.value}</span>`;
        } else {
            div.innerHTML = `<strong>${field.label}:</strong> <span>${field.value}</span>`;
        }
        
        contactInfo.appendChild(div);
    });
}

// Display Stats
function displayStats(wordCount, fileSize) {
    const stats = document.getElementById('stats');
    stats.innerHTML = '';
    
    const fileSizeKB = (fileSize / 1024).toFixed(2);
    
    const statItems = [
        { label: 'Word Count', value: wordCount + ' words' },
        { label: 'File Size', value: fileSizeKB + ' KB' },
        { label: 'Length Assessment', value: getLengthAssessment(wordCount) }
    ];
    
    statItems.forEach(item => {
        const div = document.createElement('div');
        div.className = 'stat-item';
        div.innerHTML = `
            <span class="stat-label">${item.label}</span>
            <span class="stat-value">${item.value}</span>
        `;
        stats.appendChild(div);
    });
}

function getLengthAssessment(wordCount) {
    if (wordCount < 250) return 'Too Short';
    if (wordCount > 1000) return 'Too Long';
    return 'Optimal';
}

// Display Keywords
function displayKeywords(keywords) {
    const keywordsContainer = document.getElementById('keywordsContainer');
    keywordsContainer.innerHTML = '';
    
    if (keywords.length === 0) {
        keywordsContainer.innerHTML = '<p style="color: #9ca3af;">No relevant keywords found. Add technical skills and certifications to your resume.</p>';
        return;
    }
    
    keywords.forEach(keyword => {
        const tag = document.createElement('span');
        tag.className = 'keyword-tag';
        tag.textContent = keyword;
        keywordsContainer.appendChild(tag);
    });
}

// Display Findings
function displayFindings(findings) {
    const findingsContainer = document.getElementById('findingsContainer');
    findingsContainer.innerHTML = '';
    
    if (findings.length === 0) {
        findingsContainer.innerHTML = '<p style="color: #10b981; font-weight: bold;">✓ No major issues found! Your resume looks ATS-friendly.</p>';
        return;
    }
    
    // Sort findings by severity
    const severityOrder = { high: 0, medium: 1, low: 2 };
    findings.sort((a, b) => severityOrder[a.severity] - severityOrder[b.severity]);
    
    findings.forEach(finding => {
        const div = document.createElement('div');
        div.className = `finding ${finding.severity}`;
        
        const iconMap = {
            high: '⚠️',
            medium: '⚡',
            low: 'ℹ️'
        };
        
        div.innerHTML = `
            <div class="finding-title">
                <span>${iconMap[finding.severity]} ${finding.issue}</span>
                <span class="finding-severity">${finding.severity.toUpperCase()}</span>
            </div>
            <div class="finding-suggestion">${finding.suggestion}</div>
        `;
        
        findingsContainer.appendChild(div);
    });
}

// Load Tips
function loadTips() {
    fetch('/api/ats-tips')
        .then(response => response.json())
        .then(data => {
            displayTips(data);
        })
        .catch(error => console.error('Error loading tips:', error));
}

// Display Tips
function displayTips(tipsData) {
    // Display Dos
    const dosList = document.getElementById('dosList');
    tipsData.dos.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        dosList.appendChild(li);
    });
    
    // Display Don'ts
    const dontsList = document.getElementById('dontsList');
    tipsData.donts.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        dontsList.appendChild(li);
    });
    
    // Display Keywords
    const keywordsList = document.getElementById('keywordsList');
    tipsData.keywords.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        keywordsList.appendChild(li);
    });
}

// Smooth scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTips();
});
