from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict

class SkillMatcher:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def match_skills(self, resume_skills: List[str], required_skills: List[str]) -> Dict:
        if not resume_skills or not required_skills:
            return {
                'match_percentage': 0.0,
                'matched_skills': [],
                'missing_skills': required_skills,
                'additional_skills': resume_skills
            }

        resume_embeddings = self.model.encode(resume_skills)
        required_embeddings = self.model.encode(required_skills)
        similarity_matrix = cosine_similarity(required_embeddings, resume_embeddings)

        matched_skills = []
        missing_skills = []
        threshold = 0.7

        for idx, req_skill in enumerate(required_skills):
            max_sim = similarity_matrix[idx].max()
            if max_sim >= threshold:
                best_match_idx = similarity_matrix[idx].argmax()
                matched_skills.append({
                    'required': req_skill,
                    'matched': resume_skills[best_match_idx],
                    'similarity': float(max_sim)
                })
            else:
                missing_skills.append(req_skill)

        match_percentage = (len(matched_skills) / len(required_skills)) * 100
        matched_resume_skills = [m['matched'] for m in matched_skills]
        additional_skills = [s for s in resume_skills if s not in matched_resume_skills]

        return {
            'match_percentage': round(match_percentage, 2),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'additional_skills': additional_skills,
            'total_required': len(required_skills),
            'total_matched': len(matched_skills)
        }
