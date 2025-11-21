import google.generativeai as genai
from typing import Dict, List
import json

class LLMEngine:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_resume(self, resume_data: Dict, job_data: Dict) -> Dict:
        prompt = f"""
        You are an expert HR recruiter. Analyze the following candidate resume against the job requirements.

        **Candidate Information:**
        - Name: {resume_data.get('name', 'Unknown')}
        - Skills: {', '.join(resume_data.get('skills', []))}
        - Experience: {resume_data.get('total_experience', 0)} years
        - Education: {', '.join(resume_data.get('education', []))}
        - Certifications: {', '.join(resume_data.get('certifications', []))}

        **Job Requirements:**
        - Title: {job_data['job_title']}
        - Required Skills: {', '.join(job_data['required_skills'])}
        - Experience Required: {job_data['experience_required']} years
        - Education Required: {job_data['education_required']}

        Provide:
        1. **Overall Assessment** (2-3 sentences)
        2. **Strengths** (bullet points)
        3. **Weaknesses** (bullet points)
        4. **Recommendations for Candidate** (how to improve)
        5. **Hiring Recommendation** (Yes/No/Maybe with brief reason)

        Format your response as JSON with these exact keys: overall_assessment, strengths, weaknesses, recommendations, hiring_recommendation
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text

            try:
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0]
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0]
                result = json.loads(text.strip())
            except:
                result = {
                    'overall_assessment': text[:300],
                    'strengths': ['Analysis available in full text'],
                    'weaknesses': ['See detailed response'],
                    'recommendations': ['Refer to complete analysis'],
                    'hiring_recommendation': 'See full analysis',
                    'full_text': text
                }
            return result
        except Exception as e:
            return {
                'error': str(e),
                'overall_assessment': 'Unable to generate LLM analysis',
                'strengths': [],
                'weaknesses': [],
                'recommendations': [],
                'hiring_recommendation': 'Analysis unavailable'
            }

    def generate_rejection_email(self, candidate_name: str, weaknesses: List[str]) -> str:
        prompt = f"""Write a professional, empathetic rejection email for candidate {candidate_name}.
        Areas for improvement: {chr(10).join(f'- {w}' for w in weaknesses)}
        Keep it professional, encouraging, and brief (under 150 words)."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return f"Dear {candidate_name},\n\nThank you for your interest. While we appreciate your application, we have decided to move forward with other candidates at this time.\n\nBest regards"

    def generate_interview_questions(self, resume_data: Dict, job_data: Dict) -> List[str]:
        prompt = f"""Generate 5 specific interview questions for a candidate applying for {job_data['job_title']}.
        Candidate has: Skills: {', '.join(resume_data.get('skills', [])[:5])}, Experience: {resume_data.get('total_experience', 0)} years
        Questions should be technical and behavioral mix. Return as JSON array of strings."""

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            questions = json.loads(text.strip())
            return questions if isinstance(questions, list) else []
        except:
            return [
                "Tell me about your relevant experience.",
                "What are your key technical strengths?",
                "Describe a challenging project you worked on.",
                "Why are you interested in this role?",
                "Where do you see yourself in 5 years?"
            ]
