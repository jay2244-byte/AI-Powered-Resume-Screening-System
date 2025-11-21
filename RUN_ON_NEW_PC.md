# 🚀 How to Run This Project on a New Computer

Follow these steps to set up the **AI-Powered Resume Screening System** on a fresh machine.

---

## 📋 Prerequisites
Before starting, ensure you have the following installed:
1. **Python 3.8+**: [Download Here](https://www.python.org/downloads/)
2. **MongoDB Community Server**: [Download Here](https://www.mongodb.com/try/download/community)
   - *Important:* Make sure MongoDB is running as a service.

---

## 🛠️ Step-by-Step Setup Commands

### 1. Open Terminal (Command Prompt / PowerShell)
Navigate to the project folder where you copied the files.
```powershell
cd "path\to\AI-Powered Resume Screening System"
```

### 2. Create a Virtual Environment
This keeps your project dependencies isolated.
```powershell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```
*(You should see `(venv)` appear at the start of your command line)*

### 3. Install Dependencies
Install all required Python libraries.
```powershell
pip install -r requirements.txt
```

### 4. Download Language Model
Download the required NLP model for spaCy.
```powershell
python -m spacy download en_core_web_sm
```

### 5. Configure Environment Variables
Create a new file named `.env` inside the `backend` folder and add your keys.
```powershell
# Create .env file (or create it manually in Notepad)
echo GOOGLE_API_KEY=your_actual_api_key_here > backend\.env
echo MONGO_URI=mongodb://localhost:27017/ >> backend\.env
echo SQL_URI=sqlite:///./resume_db.sqlite >> backend\.env
```
⚠️ **Important:** Open `backend\.env` and replace `your_actual_api_key_here` with your real Google Gemini API Key.

---

## 🏃‍♂️ How to Run the App

You need to run **two separate terminals** (don't forget to activate `venv` in both!).

### Terminal 1: Start Backend
```powershell
.\venv\Scripts\activate
python backend\app.py
```

### Terminal 2: Start Frontend
```powershell
.\venv\Scripts\activate
streamlit run frontend\streamlit_app.py
```

---

## 🌐 Access the App
- **Frontend:** http://localhost:8501
- **Backend:** http://localhost:8000
