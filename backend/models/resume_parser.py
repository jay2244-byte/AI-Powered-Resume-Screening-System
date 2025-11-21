import PyPDF2
import pdfplumber
import docx
import re
import spacy
from typing import Dict, List
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        self.stop_words = set(stopwords.words('english'))
        self.common_skills = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'git', 'agile', 'scrum', 'devops', 'ci/cd',
            'html', 'css', 'rest api', 'graphql', 'microservices'
        ]

    def extract_text(self, file_path: str) -> str:
        text = ""
        if file_path.endswith('.pdf'):
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() or ""
            except:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
        elif file_path.endswith('.docx'):
            doc = docx.Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        return text

    def extract_name(self, text: str) -> str:
        doc = self.nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return "Unknown"

    def extract_email(self, text: str) -> str:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""

    def extract_phone(self, text: str) -> str:
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return ''.join(phones[0]) if phones else ""

    def extract_skills(self, text: str) -> List[str]:
        text_lower = text.lower()
        found_skills = []
        for skill in self.common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return list(set(found_skills))

    def extract_experience(self, text: str) -> Dict:
        exp_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'experience\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)',
        ]
        total_years = 0
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                total_years = max([int(m) for m in matches])
                break
        return {'total_experience': total_years, 'details': []}

    def extract_education(self, text: str) -> List[str]:
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'diploma',
            'b.tech', 'm.tech', 'b.e', 'm.e', 'bsc', 'msc',
            'bba', 'mba', 'b.com', 'm.com'
        ]
        text_lower = text.lower()
        found_education = []
        for keyword in education_keywords:
            if keyword in text_lower:
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                matches = re.findall(pattern, text_lower)
                if matches:
                    found_education.extend(matches)
        return list(set(found_education))

    def extract_certifications(self, text: str) -> List[str]:
        cert_keywords = [
            'certified', 'certification', 'certificate',
            'aws certified', 'azure certified', 'google certified',
            'pmp', 'cissp', 'comptia', 'ccna', 'ceh'
        ]
        text_lower = text.lower()
        found_certs = []
        for keyword in cert_keywords:
            if keyword in text_lower:
                pattern = rf'.{{0,50}}{keyword}.{{0,50}}'
                matches = re.findall(pattern, text_lower)
                if matches:
                    found_certs.extend(matches)
        return list(set(found_certs))

    def parse_resume(self, file_path: str) -> Dict:
        text = self.extract_text(file_path)
        if not text:
            raise ValueError("Could not extract text from resume")

        parsed_data = {
            'raw_text': text,
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'total_experience': self.extract_experience(text)['total_experience'],
            'education': self.extract_education(text),
            'certifications': self.extract_certifications(text)
        }
        return parsed_data
