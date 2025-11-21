from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict, List, Optional

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    resume_id = Column(String(100))
    name = Column(String(200))
    email = Column(String(200))
    job_title = Column(String(200))
    skill_match_score = Column(Float)
    ml_prediction = Column(String(50))
    confidence_score = Column(Float)
    overall_score = Column(Float)
    bias_detected = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class SQLDatabase:
    def __init__(self, uri: str):
        self.engine = create_engine(uri)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)
        print("✅ SQL tables created")

    def store_candidate_score(self, data: Dict) -> int:
        session = self.SessionLocal()
        try:
            candidate = Candidate(**data)
            session.add(candidate)
            session.commit()
            session.refresh(candidate)
            return candidate.id
        finally:
            session.close()

    def get_all_candidates(self, limit: int = 50) -> List[Dict]:
        session = self.SessionLocal()
        try:
            candidates = session.query(Candidate).order_by(
                Candidate.timestamp.desc()
            ).limit(limit).all()

            return [{
                'id': c.id,
                'name': c.name,
                'email': c.email,
                'job_title': c.job_title,
                'overall_score': c.overall_score,
                'ml_prediction': c.ml_prediction,
                'timestamp': c.timestamp.isoformat()
            } for c in candidates]
        finally:
            session.close()

    def get_candidate_by_id(self, candidate_id: int) -> Optional[Dict]:
        session = self.SessionLocal()
        try:
            candidate = session.query(Candidate).filter(
                Candidate.id == candidate_id
            ).first()

            if not candidate:
                return None

            return {
                'id': candidate.id,
                'resume_id': candidate.resume_id,
                'name': candidate.name,
                'email': candidate.email,
                'job_title': candidate.job_title,
                'skill_match_score': candidate.skill_match_score,
                'ml_prediction': candidate.ml_prediction,
                'confidence_score': candidate.confidence_score,
                'overall_score': candidate.overall_score,
                'bias_detected': candidate.bias_detected,
                'timestamp': candidate.timestamp.isoformat()
            }
        finally:
            session.close()

    def get_training_data(self) -> List[Dict]:
        session = self.SessionLocal()
        try:
            candidates = session.query(Candidate).all()
            return []
        finally:
            session.close()
