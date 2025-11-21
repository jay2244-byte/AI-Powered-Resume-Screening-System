from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List
import os
import tempfile
from datetime import datetime

from models.resume_parser import ResumeParser
from models.skill_matcher import SkillMatcher
from models.ml_classifier import MLClassifier
from models.bias_detector import BiasDetector
from models.llm_engine import LLMEngine
from database.mongo_db import MongoDB
from database.sql_db import SQLDatabase
from config import Config

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await mongo_db.connect()
    sql_db.create_tables()
    print("✅ Application started successfully")
    yield
    # Shutdown
    await mongo_db.disconnect()
    print("👋 Application shutdown")

app = FastAPI(title="AI Resume Screening API", version="1.0.0", lifespan=lifespan)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
config = Config()
resume_parser = ResumeParser()
skill_matcher = SkillMatcher()
ml_classifier = MLClassifier()
bias_detector = BiasDetector()
llm_engine = LLMEngine(config.GOOGLE_API_KEY)
mongo_db = MongoDB(config.MONGO_URI, config.MONGO_DB)
sql_db = SQLDatabase(config.SQL_URI)

@app.get("/")
async def root():
    return {"message": "AI Resume Screening API is running", "version": "1.0.0"}

@app.post("/api/screen-resume")
async def screen_resume(
    resume: UploadFile = File(...),
    job_title: str = Form(...),
    required_skills: str = Form(...),
    experience_required: float = Form(...),
    education_required: str = Form(...),
    job_description: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume.filename)[1]) as tmp_file:
            content = await resume.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        parsed_data = resume_parser.parse_resume(tmp_file_path)
        bias_report = bias_detector.detect_bias(parsed_data)
        cleaned_data = bias_detector.remove_sensitive_info(parsed_data)

        skills_list = [s.strip() for s in required_skills.split(',')]
        skill_match_result = skill_matcher.match_skills(
            cleaned_data.get('skills', []),
            skills_list
        )

        features = ml_classifier.extract_features(
            cleaned_data,
            skill_match_result['match_percentage'],
            experience_required
        )
        ml_prediction = ml_classifier.predict(features)

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

        explanation = ml_classifier.explain_prediction(features)

        resume_id = await mongo_db.store_resume({
            'filename': resume.filename,
            'parsed_data': parsed_data,
            'cleaned_data': cleaned_data,
            'timestamp': datetime.utcnow()
        })

        candidate_id = sql_db.store_candidate_score({
            'resume_id': str(resume_id),
            'name': cleaned_data.get('name', 'Unknown'),
            'email': cleaned_data.get('email', ''),
            'job_title': job_title,
            'skill_match_score': skill_match_result['match_percentage'],
            'ml_prediction': ml_prediction['label'],
            'confidence_score': ml_prediction['confidence'],
            'overall_score': (skill_match_result['match_percentage'] + ml_prediction['confidence'] * 100) / 2,
            'bias_detected': bias_report['has_bias'],
            'timestamp': datetime.utcnow()
        })

        os.unlink(tmp_file_path)

        response = {
            'success': True,
            'candidate_id': candidate_id,
            'resume_id': str(resume_id),
            'parsed_info': {
                'name': cleaned_data.get('name', 'Unknown'),
                'email': cleaned_data.get('email', ''),
                'phone': cleaned_data.get('phone', ''),
                'skills': cleaned_data.get('skills', []),
                'experience_years': cleaned_data.get('total_experience', 0),
                'education': cleaned_data.get('education', []),
                'certifications': cleaned_data.get('certifications', [])
            },
            'skill_analysis': skill_match_result,
            'ml_prediction': ml_prediction,
            'llm_insights': llm_analysis,
            'bias_report': bias_report,
            'explanation': explanation,
            'final_recommendation': {
                'decision': ml_prediction['label'],
                'overall_score': round((skill_match_result['match_percentage'] + ml_prediction['confidence'] * 100) / 2, 2),
                'confidence': ml_prediction['confidence']
            }
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.get("/api/candidates")
async def get_candidates(limit: int = 50):
    candidates = sql_db.get_all_candidates(limit)
    return {"success": True, "candidates": candidates}

@app.get("/api/candidate/{candidate_id}")
async def get_candidate_detail(candidate_id: int):
    candidate = sql_db.get_candidate_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    resume_data = await mongo_db.get_resume(candidate['resume_id'])

    return {
        'success': True,
        'candidate': candidate,
        'full_resume_data': resume_data
    }

@app.post("/api/train-model")
async def train_model():
    try:
        training_data = sql_db.get_training_data()
        if len(training_data) < 50:
            raise HTTPException(status_code=400, detail="Not enough data for training (minimum 50 samples)")

        metrics = ml_classifier.train_model(training_data)
        return {"success": True, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
