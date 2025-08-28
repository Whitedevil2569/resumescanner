# ai_resume_scanner.py
import streamlit as st
import docx2txt
import PyPDF2
import re

# ------------------------------
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text() + " "
    return text

# ------------------------------
# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    return docx2txt.process(docx_file)

# ------------------------------
# Function to analyze resume vs job description
def analyze_resume(resume_text, job_description):
    score = 0
    # Basic keyword extraction
    jd_keywords = re.findall(r'\b\w+\b', job_description.lower())
    # Improved synonym expansion and matching
    synonym_dict = {
        'communication': ['communicate', 'present', 'presentation', 'verbal', 'written', 'listening'],
        'leadership': ['lead', 'manage', 'team lead', 'supervise', 'mentoring', 'guidance'],
        'teamwork': ['collaboration', 'cooperation', 'team player', 'group work', 'partnership'],
        'problem': ['issue', 'challenge', 'troubleshoot', 'problem solving', 'resolve'],
        'solution': ['solve', 'resolve', 'fix', 'solution oriented'],
        'adaptability': ['flexibility', 'adjust', 'adapt', 'versatile'],
        'creativity': ['innovative', 'creative', 'imagination', 'originality'],
        'time': ['time management', 'punctual', 'deadline', 'schedule'],
        'organization': ['organize', 'organizational', 'planning', 'arrange'],
        'motivation': ['motivated', 'self-motivated', 'initiative', 'drive'],
        'work ethic': ['dedicated', 'commitment', 'responsibility', 'reliable', 'dependable'],
        'interpersonal': ['relationship', 'people skills', 'rapport', 'empathy'],
        'conflict': ['dispute', 'resolution', 'mediate', 'negotiation'],
        'attention': ['detail', 'meticulous', 'thorough', 'accuracy'],
        'decision': ['decision making', 'judgment', 'evaluate'],
        'customer': ['client', 'customer service', 'support', 'service'],
        'presentation': ['public speaking', 'present', 'demonstration'],
        'multitasking': ['multi-tasking', 'juggle', 'simultaneous'],
        'empathy': ['understanding', 'compassion', 'considerate'],
        'negotiation': ['bargain', 'deal', 'mediate'],
        'collaboration': ['cooperate', 'teamwork', 'work together'],
        'initiative': ['proactive', 'self-starter', 'take charge'],
        'responsibility': ['accountable', 'ownership', 'reliable'],
        'flexibility': ['adaptability', 'versatile', 'adjust'],
        'developer': ['programmer', 'coder', 'engineer', 'dev'],
        'engineer': ['developer', 'programmer', 'coder', 'devops', 'architect'],
        'python': ['py', 'python3', 'python2'],
        'java': ['jdk', 'jre', 'spring', 'hibernate'],
        'manager': ['lead', 'supervisor', 'scrum master', 'product owner'],
        'sql': ['database', 'db', 'mysql', 'postgres', 'oracle', 'mssql', 'sqlite'],
        'javascript': ['js', 'nodejs', 'ecmascript', 'typescript'],
        'typescript': ['ts'],
        'analyst': ['analytics', 'analysis', 'business analyst', 'ba'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud computing', 'cloud engineer'],
        'frontend': ['front-end', 'ui', 'web', 'html', 'css', 'javascript', 'react', 'angular', 'vue'],
        'backend': ['back-end', 'server', 'api', 'database', 'node', 'django', 'flask', 'spring'],
        'fullstack': ['full-stack', 'frontend', 'backend'],
        'machine': ['ml', 'ai', 'machine learning', 'deep learning'],
        'learning': ['ml', 'ai', 'machine learning', 'deep learning'],
        'data': ['dataset', 'database', 'data science', 'data analyst', 'big data', 'etl'],
        'project': ['assignment', 'task', 'project management', 'agile', 'scrum'],
        'testing': ['qa', 'test', 'automation', 'selenium', 'junit', 'pytest'],
        'support': ['help', 'assist', 'technical support', 'it support'],
        'administrator': ['admin', 'sysadmin', 'system administrator', 'network admin'],
        'designer': ['design', 'ui', 'ux', 'graphic', 'web designer'],
        'react': ['reactjs', 'react native'],
        'angular': ['angularjs', 'angular 2+'],
        'node': ['nodejs', 'express'],
        'c++': ['cpp', 'cplusplus'],
        'c#': ['dotnet', '.net', 'asp.net'],
        'excel': ['spreadsheet', 'ms excel'],
        'powerpoint': ['presentation', 'ms powerpoint'],
        'team': ['group', 'squad', 'teamwork'],
        'docker': ['container', 'containers', 'kubernetes', 'k8s'],
        'linux': ['unix', 'ubuntu', 'centos', 'redhat', 'shell', 'bash'],
        'windows': ['win32', 'win64', 'microsoft'],
        'api': ['rest', 'restful', 'graphql', 'web service'],
        'mobile': ['android', 'ios', 'app', 'mobile app'],
        'security': ['cybersecurity', 'infosec', 'pentest', 'vulnerability'],
        'devops': ['ci', 'cd', 'jenkins', 'docker', 'kubernetes', 'automation'],
        'etl': ['extract', 'transform', 'load', 'data pipeline'],
        'bigdata': ['hadoop', 'spark', 'hive', 'pig'],
        'ai': ['artificial intelligence', 'ml', 'machine learning'],
        'nlp': ['natural language processing', 'text mining'],
        'scrum': ['agile', 'scrum master'],
        'agile': ['scrum', 'kanban'],
        'git': ['version control', 'github', 'gitlab', 'bitbucket'],
        'network': ['networking', 'tcp/ip', 'udp', 'firewall', 'router'],
        'hardware': ['firmware', 'embedded', 'iot'],
        'qa': ['quality assurance', 'testing', 'test'],
    }
    # Build a set of all keywords and their synonyms (flattened)
    expanded_keywords = set(jd_keywords)
    for word in jd_keywords:
        for key, syns in synonym_dict.items():
            if word == key or word in syns:
                expanded_keywords.add(key)
                expanded_keywords.update(syns)
    # Also add all synonyms for any direct match
    for word in list(expanded_keywords):
        if word in synonym_dict:
            expanded_keywords.update(synonym_dict[word])
    # For phrase matching, join resume text as a string
    resume_text_lower = resume_text.lower()
    resume_words = set(re.findall(r'\b\w+\b', resume_text_lower))
    matched_keywords = set()
    for kw in expanded_keywords:
        if ' ' in kw:
            if kw in resume_text_lower:
                matched_keywords.add(kw)
        else:
            if kw in resume_words:
                matched_keywords.add(kw)
    score = len(matched_keywords)
    return score, matched_keywords

# ------------------------------
# Streamlit Web App

# --- Custom CSS for card style ---
st.markdown("""
    <style>
    body, .stApp {
        background: rgba(255,255,255,0.4) !important;
        color: #232526 !important;
    }
    .card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.13);
        padding: 1.5em 1em 1em 1em;
        margin-bottom: 1.5em;
        border: 1px solid #fcb69f;
    }
    .score {
        color: #d72660;
        font-weight: bold;
        font-size: 1.15em;
        letter-spacing: 0.5px;
    }
    .keywords {
        color: #1b998b;
        font-size: 1em;
        font-weight: 500;
    }
    .stTextInput > div > div > input, .stTextArea textarea {
        background: #fff !important;
        color: #232526 !important;
        border-radius: 8px;
        border: 1px solid #fcb69f;
    }
    .stButton > button {
        background: #d72660 !important;
        color: #fff !important;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stButton > button:hover {
        background: #1b998b !important;
        color: #fff !important;
    }
    .stExpanderHeader {
        color: #d72660 !important;
    }
    </style>
""", unsafe_allow_html=True)
 
# --- Sidebar ---
st.sidebar.title("Description")
st.sidebar.info("You can upload and scan multiple resumes at one time. Supported formats: PDF, DOCX.")

st.title("📄 AI Resume Scanner,Analyser & Shortlister")

job_description = st.text_area("Paste the Job Description here")
uploaded_files = st.file_uploader("Upload Resumes (PDF/DOCX)", accept_multiple_files=True)

if st.button("Analyze Resumes"):
    results = []
    resume_texts = {}
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)
        else:
            resume_text = uploaded_file.read().decode("utf-8")

        score, matched_keywords = analyze_resume(resume_text, job_description)
        results.append((uploaded_file.name, score, matched_keywords))
        resume_texts[uploaded_file.name] = resume_text

    # Sort by score
    results.sort(key=lambda x: x[1], reverse=True)

    st.subheader("📋 Shortlisted Candidates")
    if not results:
        st.info("No resumes uploaded.")
    else:
        cols = st.columns(2)
        for idx, res in enumerate(results):
            with cols[idx % 2]:
                st.markdown(f'<div class="card">', unsafe_allow_html=True)
                st.markdown(f"<span class='score'>**{res[0]}** - Score: {res[1]}</span>", unsafe_allow_html=True)
                st.markdown(f"<div class='keywords'>✅ Matched Keywords: {', '.join(list(res[2])[:10])} ...</div>", unsafe_allow_html=True)
                if res[1] >= 4:
                    with st.expander(f"View Resume: {res[0]}"):
                        st.write(resume_texts[res[0]])
                st.markdown('</div>', unsafe_allow_html=True)
