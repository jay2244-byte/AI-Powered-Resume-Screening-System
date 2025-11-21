# Dataset Folder

## Purpose
This folder contains sample data and scripts for generating test data for the resume screening system.

## Files

### sample_data.py
Python script to generate sample candidate and job description data.

**Usage:**
```bash
python sample_data.py
```

This will create `sample_candidates.json` with:
- 50 sample candidate profiles
- 10 sample job descriptions

## Creating Custom Test Data

You can modify `sample_data.py` to:
1. Add more names, skills, job titles
2. Adjust the number of candidates
3. Customize education levels and certifications

## Real Resume Data

To use real resumes:
1. Place PDF/DOCX files in this folder
2. Use the web interface to upload and screen them
3. Data will be stored in MongoDB and PostgreSQL

## Dataset Structure

### Candidate Profile
```json
{
  "name": "John Smith",
  "email": "john.smith@email.com",
  "phone": "+1-555-123-4567",
  "skills": ["Python", "Machine Learning", "Docker"],
  "total_experience": 5,
  "education": ["B.Tech in Computer Science"],
  "certifications": ["AWS Certified"]
}
```

### Job Description
```json
{
  "job_title": "Software Engineer",
  "required_skills": ["Python", "FastAPI", "Docker"],
  "experience_required": 3,
  "education_required": "Bachelor's",
  "description": "Looking for a skilled engineer..."
}
```
