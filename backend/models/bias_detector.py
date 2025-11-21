from typing import Dict, List
import re
from config import Config

class BiasDetector:
    def __init__(self):
        self.sensitive_keywords = Config.SENSITIVE_KEYWORDS
        self.bias_patterns = {
            'gender': r'\b(male|female|man|woman|boy|girl|he|she|gender)\b',
            'age': r'\b(age|years old|\d+\s*years old|born in|dob|date of birth)\b',
            'religion': r'\b(muslim|christian|hindu|jewish|buddhist|sikh|religion|religious)\b',
            'marital_status': r'\b(married|single|divorced|widowed|marital status)\b',
            'ethnicity': r'\b(african|asian|caucasian|hispanic|latino|ethnicity|race)\b',
            'disability': r'\b(disabled|disability|handicapped|impairment)\b'
        }

    def detect_bias(self, resume_data: Dict) -> Dict:
        raw_text = resume_data.get('raw_text', '').lower()
        detected_biases = {}
        bias_count = 0

        for bias_type, pattern in self.bias_patterns.items():
            matches = re.findall(pattern, raw_text, re.IGNORECASE)
            if matches:
                detected_biases[bias_type] = {
                    'found': True,
                    'matches': list(set(matches)),
                    'count': len(matches)
                }
                bias_count += 1
            else:
                detected_biases[bias_type] = {'found': False}

        return {
            'has_bias': bias_count > 0,
            'total_bias_types': bias_count,
            'details': detected_biases,
            'risk_level': 'high' if bias_count >= 3 else 'medium' if bias_count >= 1 else 'low'
        }

    def remove_sensitive_info(self, resume_data: Dict) -> Dict:
        cleaned_data = resume_data.copy()
        if 'raw_text' in cleaned_data:
            text = cleaned_data['raw_text']
            for keyword in self.sensitive_keywords:
                text = re.sub(rf'\b{keyword}\b', '[REDACTED]', text, flags=re.IGNORECASE)
            text = re.sub(r'\b\d{1,2}\s*years\s*old\b', '[AGE_REDACTED]', text, flags=re.IGNORECASE)
            text = re.sub(r'\bborn\s*in\s*\d{4}\b', '[DOB_REDACTED]', text, flags=re.IGNORECASE)
            text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DATE_REDACTED]', text)
            cleaned_data['raw_text'] = text
        return cleaned_data

    def calculate_fairness_score(self, predictions: List[Dict]) -> Dict:
        if not predictions:
            return {'fairness_score': 100.0, 'note': 'No data to analyze'}

        suitable_count = sum(1 for p in predictions if p.get('class', 0) >= 1)
        total_count = len(predictions)
        selection_rate = (suitable_count / total_count) * 100 if total_count > 0 else 0
        fairness_score = 100.0 - abs(50.0 - selection_rate)

        return {
            'fairness_score': round(fairness_score, 2),
            'selection_rate': round(selection_rate, 2),
            'total_analyzed': total_count,
            'suitable_count': suitable_count
        }
