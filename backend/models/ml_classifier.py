from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import pickle
import os
from typing import Dict, List

class MLClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'skill_match_percentage',
            'experience_years',
            'education_score',
            'certification_count',
            'skill_count'
        ]
        self.load_model()

    def extract_features(self, resume_data: Dict, skill_match: float, required_exp: float) -> np.ndarray:
        education_score = 0
        education = resume_data.get('education', [])
        if any('phd' in str(e).lower() or 'doctorate' in str(e).lower() for e in education):
            education_score = 4
        elif any('master' in str(e).lower() or 'm.tech' in str(e).lower() for e in education):
            education_score = 3
        elif any('bachelor' in str(e).lower() or 'b.tech' in str(e).lower() for e in education):
            education_score = 2
        elif any('diploma' in str(e).lower() for e in education):
            education_score = 1

        features = np.array([[
            skill_match,
            min(resume_data.get('total_experience', 0) / max(required_exp, 1), 2.0),
            education_score,
            len(resume_data.get('certifications', [])),
            len(resume_data.get('skills', []))
        ]])
        return features

    def predict(self, features: np.ndarray) -> Dict:
        if not self.is_trained:
            return self._rule_based_prediction(features)

        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        labels = ['Not Suitable', 'Moderately Suitable', 'Highly Suitable']

        return {
            'label': labels[prediction],
            'class': int(prediction),
            'confidence': float(probabilities[prediction]),
            'probabilities': {
                labels[i]: float(prob) for i, prob in enumerate(probabilities)
            }
        }

    def _rule_based_prediction(self, features: np.ndarray) -> Dict:
        skill_match = features[0][0]
        exp_ratio = features[0][1]
        education = features[0][2]
        certs = features[0][3]

        score = (skill_match * 0.4 + exp_ratio * 50 * 0.3 + 
                 education * 10 * 0.2 + min(certs * 5, 20) * 0.1)

        if score >= 70:
            label, class_idx, confidence = 'Highly Suitable', 2, min(score / 100, 0.95)
        elif score >= 50:
            label, class_idx, confidence = 'Moderately Suitable', 1, min(score / 100, 0.80)
        else:
            label, class_idx, confidence = 'Not Suitable', 0, max(1 - score / 100, 0.60)

        return {
            'label': label,
            'class': class_idx,
            'confidence': confidence,
            'probabilities': {
                'Not Suitable': 1.0 if class_idx == 0 else 0.1,
                'Moderately Suitable': 1.0 if class_idx == 1 else 0.3,
                'Highly Suitable': 1.0 if class_idx == 2 else 0.2
            }
        }

    def train_model(self, training_data: List[Dict]) -> Dict:
        if len(training_data) < 50:
            raise ValueError("Insufficient training data")

        X, y = [], []
        for data in training_data:
            features = self.extract_features(
                data['resume_data'],
                data['skill_match_score'],
                data['experience_required']
            )
            X.append(features[0])
            y.append(data['label'])

        X, y = np.array(X), np.array(y)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        self.model.fit(X_train_scaled, y_train)

        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        self.is_trained = True
        self.save_model()
        return {'accuracy': accuracy, 'classification_report': report}

    def explain_prediction(self, features: np.ndarray) -> Dict:
        explanations = []
        if features[0][0] >= 70:
            explanations.append("Strong skill match with job requirements")
        elif features[0][0] >= 50:
            explanations.append("Moderate skill match with job requirements")
        else:
            explanations.append("Low skill match with job requirements")

        if features[0][1] >= 1.0:
            explanations.append("Meets or exceeds experience requirements")
        else:
            explanations.append("Below required experience level")

        if features[0][2] >= 3:
            explanations.append("Strong educational background")

        if features[0][3] > 0:
            explanations.append(f"Has {int(features[0][3])} relevant certification(s)")

        return {
            'feature_importance': {
                self.feature_names[i]: float(features[0][i]) for i in range(len(self.feature_names))
            },
            'explanation_text': ' | '.join(explanations)
        }

    def save_model(self):
        os.makedirs('models', exist_ok=True)
        with open('models/ml_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        with open('models/scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)

    def load_model(self):
        try:
            with open('models/ml_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('models/scaler.pkl', 'rb') as f:
                self.scaler = pickle.load(f)
            self.is_trained = True
        except FileNotFoundError:
            self.is_trained = False
