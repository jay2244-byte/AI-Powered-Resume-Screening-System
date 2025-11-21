import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import asyncio

# Add project root to path so we can import from backend
import sys
import os
root_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir, 'backend'))

# Import Backend Logic
from backend.models.resume_parser import ResumeParser
from backend.models.skill_matcher import SkillMatcher
from backend.models.ml_classifier import MLClassifier
from backend.models.bias_detector import BiasDetector
from backend.models.llm_engine import LLMEngine
from backend.database.sql_db import SQLDatabase
from backend.config import Config

st.set_page_config(
    page_title="Resume Screening AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Components (Cached)
@st.cache_resource
def get_components():
    # Get API Key from Secrets (Cloud) or Config (Local)
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", Config.GOOGLE_API_KEY)
    except FileNotFoundError:
        api_key = Config.GOOGLE_API_KEY
    except Exception:
        api_key = Config.GOOGLE_API_KEY
    
    config = Config()
    resume_parser = ResumeParser()
    skill_matcher = SkillMatcher()
    ml_classifier = MLClassifier()
    bias_detector = BiasDetector()
    llm_engine = LLMEngine(api_key)
    
    # Use SQLite for Cloud Deployment (Simplest persistence)
    # Note: MongoDB requires a cloud connection string in secrets for persistence
    sql_db = SQLDatabase("sqlite:///./resume_db.sqlite")
    sql_db.create_tables()
    
    return resume_parser, skill_matcher, ml_classifier, bias_detector, llm_engine, sql_db

resume_parser, skill_matcher, ml_classifier, bias_detector, llm_engine, sql_db = get_components()

# Custom CSS for Glassmorphism and Modern UI
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphism Card Style */
    .glass-container {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }

    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
    }

    /* Custom Button Styling */
    div.stButton > button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        width: 100%;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
        background: linear-gradient(90deg, #4338ca 0%, #6d28d9 100%);
    }

    div.stButton > button:active {
        transform: translateY(0);
    }

    /* Input Fields Styling */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea, 
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        color: #1f2937;
    }

    /* Headers */
    h1, h2, h3 {
        color: #1f2937;
        font-weight: 700;
    }

    .gradient-text {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4f46e5;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    page = st.radio("", ["Screen Resume", "View Candidates", "Analytics", "About"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.5); border-radius: 10px;'>
            <p style='margin:0; font-size:0.8rem; color:#666;'>Powered by</p>
            <h4 style='margin:0; color:#4f46e5;'>Gemini AI</h4>
        </div>
    """, unsafe_allow_html=True)

if page == "Screen Resume":
    st.markdown('<h1 style="text-align: center; margin-bottom: 2rem;">✨ <span class="gradient-text">Smart Resume Screening</span></h1>', unsafe_allow_html=True)

    # Main Form Container
    with st.container():
        st.markdown('<div class="glass-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.2], gap="large")

        with col1:
            st.markdown("### 📤 Upload Resume")
            st.markdown("Drop your candidate's resume here (PDF/DOCX)")
            uploaded_file = st.file_uploader("", type=['pdf', 'docx'], label_visibility="collapsed")
            
            if uploaded_file:
                st.success(f"✅ File loaded: {uploaded_file.name}")

        with col2:
            st.markdown("### 📋 Job Details")
            job_title = st.text_input("Job Title", "Software Engineer")
            
            c1, c2 = st.columns(2)
            with c1:
                experience_required = st.number_input("Min Experience (Years)", 0.0, 20.0, 3.0, 0.5)
            with c2:
                education_required = st.selectbox("Education", ["Bachelor's", "Master's", "PhD", "Any"])
            
            required_skills = st.text_area("Required Skills", "Python, Machine Learning, FastAPI, Docker, React")
            job_description = st.text_area("Job Description", "Looking for a skilled engineer to build scalable AI systems...")

        st.markdown("</div>", unsafe_allow_html=True)

        # Action Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_btn = st.button("⚡ Analyze Resume", type="primary", use_container_width=True)

    if analyze_btn:
        if uploaded_file is None:
            st.error("⚠️ Please upload a resume to proceed.")
        else:
            with st.spinner("🔮 Analyzing candidate profile..."):
                try:
                    # Save uploaded file temporarily
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    # 1. Parse Resume
                    parsed_data = resume_parser.parse_resume(tmp_file_path)
                    os.unlink(tmp_file_path) # Clean up
                    
                    # 2. Detect Bias
                    bias_report = bias_detector.detect_bias(parsed_data)
                    cleaned_data = bias_detector.remove_sensitive_info(parsed_data)

                    # 3. Match Skills
                    skills_list = [s.strip() for s in required_skills.split(',')]
                    skill_match_result = skill_matcher.match_skills(
                        cleaned_data.get('skills', []),
                        skills_list
                    )

                    # 4. ML Classification
                    features = ml_classifier.extract_features(
                        cleaned_data,
                        skill_match_result['match_percentage'],
                        experience_required
                    )
                    ml_prediction = ml_classifier.predict(features)

                    # 5. LLM Analysis
                    llm_analysis = llm_engine.analyze_resume(
                        cleaned_data,
                        {
                            'job_title': job_title,
                            'required_skills': skills_list,
                            'experience_required': experience_required,
                            'education_required': education_required,
                            'description': job_description
                        }
                    )
                    
                    # 6. Store Results (SQLite)
                    candidate_id = sql_db.store_candidate_score({
                        'resume_id': 'local_upload', # Simplified for demo
                        'name': cleaned_data.get('name', 'Unknown'),
                        'email': cleaned_data.get('email', ''),
                        'job_title': job_title,
                        'skill_match_score': skill_match_result['match_percentage'],
                        'ml_prediction': ml_prediction['label'],
                        'confidence_score': ml_prediction['confidence'],
                        'overall_score': (skill_match_result['match_percentage'] + ml_prediction['confidence'] * 100) / 2,
                        'bias_detected': bias_report['has_bias'],
                        'timestamp': pd.Timestamp.now()
                    })

                    # Results Section
                    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                    
                    # Header Stats
                    st.markdown("### 📊 Analysis Results")
                    r_col1, r_col2, r_col3, r_col4 = st.columns(4)
                    
                    overall_score = (skill_match_result['match_percentage'] + ml_prediction['confidence'] * 100) / 2
                    
                    with r_col1:
                        st.metric("Match Score", f"{overall_score:.1f}%", delta=f"{ml_prediction['confidence']*100:.0f}% Conf.")
                    with r_col2:
                        color = "green" if ml_prediction['label'] == "Highly Suitable" else "orange"
                        st.markdown(f"**Decision**")
                        st.markdown(f"<h3 style='color: {color}; margin:0;'>{ml_prediction['label']}</h3>", unsafe_allow_html=True)
                    with r_col3:
                        st.metric("Experience", f"{parsed_data.get('total_experience', 0)} Yrs")
                    with r_col4:
                        st.metric("Skills Match", f"{skill_match_result['match_percentage']}%")

                    st.markdown("---")

                    # Detailed Analysis
                    d_col1, d_col2 = st.columns([1.5, 1])
                    
                    with d_col1:
                        st.markdown("#### 🧠 AI Insights")
                        if llm_analysis:
                            st.info(llm_analysis.get('overall_assessment', 'No insights available'))
                        
                        st.markdown("#### 🛠️ Skills Breakdown")
                        s_col1, s_col2 = st.columns(2)
                        with s_col1:
                            st.markdown("**✅ Matched**")
                            for s in skill_match_result['matched_skills'][:5]:
                                st.markdown(f"- {s['required']}")
                        with s_col2:
                            st.markdown("**❌ Missing**")
                            for s in skill_match_result['missing_skills'][:5]:
                                st.markdown(f"- {s}")

                    with d_col2:
                        st.markdown("#### 👤 Candidate Profile")
                        st.markdown(f"**Name:** {cleaned_data.get('name', 'Unknown')}")
                        st.markdown(f"**Email:** {cleaned_data.get('email', 'Unknown')}")
                        st.markdown(f"**Phone:** {cleaned_data.get('phone', 'Unknown')}")
                        
                        st.markdown("#### ⚖️ Bias Check")
                        if bias_report['has_bias']:
                            st.warning(f"⚠️ Risk: {bias_report['risk_level']}")
                        else:
                            st.success("✅ No Bias Detected")

                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    import traceback
                    st.error(traceback.format_exc())

elif page == "View Candidates":
    st.markdown('<h1 style="text-align: center;">👥 <span class="gradient-text">Candidate Database</span></h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    try:
        candidates = sql_db.get_all_candidates(100)
        if candidates:
            df = pd.DataFrame(candidates)
            st.dataframe(
                df.style.background_gradient(cmap="Blues", subset=["overall_score"]),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No candidates found yet.")
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analytics":
    st.markdown('<h1 style="text-align: center;">📈 <span class="gradient-text">Recruitment Analytics</span></h1>', unsafe_allow_html=True)
    
    try:
        candidates = sql_db.get_all_candidates(1000)
        if candidates:
            df = pd.DataFrame(candidates)
            
            # Top Stats Row
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Candidates", len(df))
            c2.metric("Avg Score", f"{df['overall_score'].mean():.1f}")
            c3.metric("Top Talent", len(df[df['ml_prediction'] == 'Highly Suitable']))
            c4.metric("Avg Experience", "N/A") 
            st.markdown("</div>", unsafe_allow_html=True)

            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                st.subheader("Score Distribution")
                fig = px.histogram(df, x="overall_score", nbins=20, color_discrete_sequence=['#4f46e5'])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                st.subheader("Suitability Breakdown")
                fig = px.pie(df, names="ml_prediction", color_discrete_sequence=px.colors.sequential.RdBu)
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No data available for analytics.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

else:
    st.markdown('<div class="glass-container" style="text-align: center;">', unsafe_allow_html=True)
    st.markdown("# ℹ️ About System")
    st.markdown("""
    ### Next-Gen Resume Screening
    Built with **FastAPI**, **Gemini AI**, and **Streamlit**.
    
    **Features:**
    - 📄 Intelligent Resume Parsing
    - 🧠 Semantic Skill Matching
    - ⚖️ Responsible AI Bias Detection
    """)
    st.markdown("</div>", unsafe_allow_html=True)
