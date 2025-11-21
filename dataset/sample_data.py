# Sample data generator for resume screening system
import random
import json
from datetime import datetime, timedelta

class SampleDataGenerator:
    def __init__(self):
        self.names = [
            "John Smith", "Emily Johnson", "Michael Brown", "Sarah Davis",
            "David Wilson", "Lisa Anderson", "Robert Taylor", "Jennifer Martinez"
        ]
        self.skills = [
            "Python", "Java", "JavaScript", "C++", "React", "Angular", "Node.js",
            "Machine Learning", "Deep Learning", "Docker", "Kubernetes", "AWS",
            "Azure", "SQL", "MongoDB", "PostgreSQL", "Git", "Agile", "Scrum"
        ]
        self.job_titles = [
            "Software Engineer", "Data Scientist", "Full Stack Developer",
            "DevOps Engineer", "ML Engineer", "Backend Developer"
        ]
        self.education_levels = [
            "B.Tech in Computer Science",
            "M.Tech in Artificial Intelligence",
            "Bachelor's in Information Technology",
            "Master's in Data Science",
            "PhD in Machine Learning"
        ]
        self.certifications = [
            "AWS Certified Solutions Architect",
            "Google Cloud Professional",
            "Azure DevOps Engineer",
            "PMP Certification",
            "Kubernetes Administrator"
        ]

    def generate_candidate(self):
        """Generate a single candidate record"""
        num_skills = random.randint(3, 8)
        candidate_skills = random.sample(self.skills, num_skills)

        return {
            "name": random.choice(self.names),
            "email": f"{random.choice(self.names).lower().replace(' ', '.')}@email.com",
            "phone": f"+1-{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
            "skills": candidate_skills,
            "total_experience": random.randint(1, 15),
            "education": [random.choice(self.education_levels)],
            "certifications": random.sample(self.certifications, random.randint(0, 2)),
            "job_title": random.choice(self.job_titles),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat()
        }

    def generate_job_description(self):
        """Generate a job description"""
        num_skills = random.randint(4, 6)
        required_skills = random.sample(self.skills, num_skills)

        return {
            "job_title": random.choice(self.job_titles),
            "required_skills": required_skills,
            "experience_required": random.randint(2, 8),
            "education_required": random.choice(["Bachelor's", "Master's", "PhD"]),
            "description": f"Looking for a {random.choice(self.job_titles)} with strong technical skills."
        }

    def generate_dataset(self, num_candidates=100):
        """Generate a dataset of candidates"""
        return [self.generate_candidate() for _ in range(num_candidates)]

    def save_to_json(self, filename="sample_candidates.json", num_candidates=100):
        """Save generated data to JSON file"""
        data = {
            "candidates": self.generate_dataset(num_candidates),
            "job_descriptions": [self.generate_job_description() for _ in range(10)]
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Generated {num_candidates} sample candidates")
        print(f"✅ Saved to {filename}")
        return data

# Example usage
if __name__ == "__main__":
    generator = SampleDataGenerator()

    # Generate and save sample data
    data = generator.save_to_json("sample_candidates.json", num_candidates=50)

    # Print sample candidate
    print("\n📋 Sample Candidate:")
    print(json.dumps(data["candidates"][0], indent=2))

    # Print sample job description
    print("\n💼 Sample Job Description:")
    print(json.dumps(data["job_descriptions"][0], indent=2))
