import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    MONGO_DB = "resume_screening"

    # PostgreSQL Configuration
    SQL_URI = os.getenv("SQL_URI", "postgresql://postgres:password@localhost:5432/resume_db")

    # Model Paths
    ML_MODEL_PATH = "models/trained_model.pkl"
    VECTORIZER_PATH = "models/vectorizer.pkl"

    # Embedding Model
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # Responsible AI Settings
    SENSITIVE_KEYWORDS = [
        'male', 'female', 'gender', 'age', 'religion', 'muslim', 'christian',
        'hindu', 'married', 'single', 'divorced', 'pregnant', 'disability'
    ]

    # Thresholds
    SKILL_MATCH_THRESHOLD = 60.0
    CLASSIFICATION_THRESHOLD = 0.7

    # Server Settings
    HOST = "0.0.0.0"
    PORT = 8000
