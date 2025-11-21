# 🎯 AI-Powered Resume Screening System

## Complete Full-Stack Web Application (ML + LLM + Responsible AI)

An intelligent recruitment assistant that automates resume screening using Machine Learning, Large Language Models, and Responsible AI principles.

---

## 📋 Features

✅ **Resume Parsing** - Extract name, email, skills, experience, education from PDF/DOCX  
✅ **Intelligent Skill Matching** - Semantic similarity using Sentence Transformers  
✅ **ML Classification** - Random Forest model (Highly/Moderately/Not Suitable)  
✅ **LLM Integration** - Google Gemini AI for deep insights & recommendations  
✅ **Bias Detection** - Identify and remove sensitive information (Responsible AI)  
✅ **Explainable AI** - LIME-based explanations for transparency  
✅ **Dual Database** - MongoDB (resume storage) + SQLite (scores/logs)  
✅ **Modern Web Dashboard** - Responsive Streamlit UI with Glassmorphism design  

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI, Python 3.8+ |
| **ML/AI** | Scikit-learn, Random Forest, LIME |
| **LLM** | Google Gemini AI |
| **NLP** | spaCy, NLTK, Sentence Transformers |
| **Embeddings** | all-MiniLM-L6-v2 |
| **Databases** | MongoDB, SQLite |
| **Frontend** | Streamlit (Modern UI) |

---

## 📁 Project Structure

```
resume-ai-screening/
├── backend/
│   ├── app.py                    # Main FastAPI application
│   ├── config.py                 # Configuration settings
│   ├── models/                   # AI/ML models
│   │   ├── resume_parser.py      # Resume parsing with NLP
│   │   ├── skill_matcher.py      # Embedding-based matching
│   │   ├── ml_classifier.py      # ML classification
│   │   ├── bias_detector.py      # Responsible AI
│   │   └── llm_engine.py         # Gemini AI integration
│   ├── database/                 # Database operations
│   │   ├── mongo_db.py           # MongoDB
│   │   └── sql_db.py             # SQLite (via SQLAlchemy)
│   ├── utils/                    # Utility functions
│   └── requirements.txt          # Dependencies
├── frontend/
│   └── streamlit_app.py          # Streamlit web interface
├── dataset/
│   └── sample_data.py            # Sample data generator
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB installed and running
- Google Gemini API key

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 2: Setup Databases

**MongoDB:**
```bash
# Start MongoDB service
mongod
```

**SQLite:**
Automatically created on first run.

### Step 3: Configure Environment
Create `.env` file in backend folder:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
MONGO_URI=mongodb://localhost:27017/
SQL_URI=sqlite:///./resume_db.sqlite
```

**Get Gemini API Key:** https://makersuite.google.com/app/apikey

### Step 4: Start Backend
```bash
cd backend
python app.py
```
✅ Backend runs on: **http://localhost:8000**

### Step 5: Start Frontend
```bash
cd frontend
streamlit run streamlit_app.py
```
✅ Frontend runs on: **http://localhost:8501**

---

## 📖 Usage

1. Open **http://localhost:8501** in your browser
2. Navigate to **"Screen Resume"** page
3. Upload a resume (PDF or DOCX)
4. Enter job requirements:
   - Job Title
   - Required Skills (comma-separated)
   - Experience Required (years)
   - Education Required
   - Job Description
5. Click **"Screen Resume"**
6. View comprehensive analysis

---

## 🔌 API Endpoints

```
POST /api/screen-resume
  - Screen a resume against job requirements

GET /api/candidates
  - Get all screened candidates

GET /api/candidate/{id}
  - Get specific candidate details

POST /api/train-model
  - Train ML model (requires 50+ samples)
```

---

## 🧪 Testing

### Create a Sample Resume
Include:
- Name, email, phone
- Skills (e.g., Python, Machine Learning, Docker)
- Experience (e.g., "3 years of experience")
- Education (e.g., "B.Tech in Computer Science")
- Optional: Certifications

### Sample Job Requirements
```
Job Title: Software Engineer
Skills: Python, Machine Learning, FastAPI, Docker
Experience: 3 years
Education: Bachelor's
```

---

## 🎯 Key Components

### 1. Resume Parser
- Extracts text from PDF/DOCX
- Uses spaCy for name extraction
- Regex patterns for email, phone, experience
- Keyword matching for skills

### 2. Skill Matcher
- Sentence Transformers embeddings
- Cosine similarity calculation
- Match percentage with detailed breakdown

### 3. ML Classifier
- Random Forest model
- Features: skill match, experience, education, certifications
- LIME for explainability

### 4. Bias Detector (Responsible AI)
- Detects: gender, age, religion, marital status, ethnicity, disability
- Redacts sensitive information
- Fairness metrics

### 5. LLM Engine
- Google Gemini AI integration
- Generates insights, recommendations
- Interview questions
- Rejection emails

---

## 📊 Database Schema

### MongoDB - `resumes` collection
```json
{
  "_id": "ObjectId",
  "filename": "resume.pdf",
  "parsed_data": {...},
  "cleaned_data": {...},
  "timestamp": "ISO-8601"
}
```

### SQLite - `candidates` table
```sql
id, resume_id, name, email, job_title,
skill_match_score, ml_prediction, confidence_score,
overall_score, bias_detected, timestamp
```

---

## 🐛 Troubleshooting

**MongoDB connection error?**
```bash
mongod --dbpath /path/to/data
```

**spaCy model not found?**
```bash
python -m spacy download en_core_web_sm
```

**Gemini API error?**
- Verify API key in .env
- Check API quota/limits

---

## 🎓 Perfect for BTech Final Year Project

### Project Highlights
✅ Full-stack development  
✅ Machine Learning implementation  
✅ LLM integration  
✅ Responsible AI (ethical considerations)  
✅ Explainable AI (transparency)  
✅ Real-world application  
✅ Scalable architecture  

### Report Structure
1. Introduction - Problem statement
2. Literature Review - Existing solutions
3. System Design - Architecture diagrams
4. Implementation - Technologies, algorithms
5. Results & Analysis - Screenshots, metrics
6. Conclusion - Achievements, future scope

---

## 🔮 Future Enhancements

- Email integration for automated communication
- Interview scheduling system
- Advanced analytics and reports
- Multi-language support
- Authentication & role-based access
- Mobile app
- Custom fine-tuned models

---

## 📝 License

Educational purposes (BTech Final Year Project)

---

## 🙏 Acknowledgments

- spaCy, Sentence Transformers, Google Gemini AI
- FastAPI, Streamlit, Scikit-learn
- MongoDB, SQLite

---

**Made with ❤️ for BTech Final Year Project 2025**

For detailed documentation, check individual module files.
