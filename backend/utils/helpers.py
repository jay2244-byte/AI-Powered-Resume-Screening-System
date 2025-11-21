# Helper utility functions

def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def format_phone(phone: str) -> str:
    import re
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def calculate_match_score(matched: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((matched / total) * 100, 2)

def extract_years_of_experience(text: str) -> int:
    import re
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'experience\s*:?\s*(\d+)\+?\s*(?:years?|yrs?)'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return max([int(m) for m in matches])
    return 0

def sanitize_text(text: str) -> str:
    import re
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)
    return text.strip()
