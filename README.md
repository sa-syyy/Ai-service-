🚀 AI Audit Backend System
📌 Overview
This project is a Flask-based backend that uses AI to:

Analyze audit data

Generate recommendations

Create full audit reports

⚙️ Tech Stack
Python (Flask)

REST APIs

Groq AI (LLM)

Postman (API testing)

Git & GitHub

📂 Project Structure
ai-service/
│── app.py
│── routes/
│   ├── describe.py
│   ├── recommend.py
│   ├── report.py
│── services/
│   ├── groq_client.py
│── prompts/
│   ├── describe.txt
│   ├── recommend.txt
│   ├── report.txt
🚀 How to Run
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Run server
python app.py
3️⃣ Server runs on
http://127.0.0.1:5000
📡 API Endpoints
🔹 1. Describe API
POST /describe

Body:

{
  "input": "audit data"
}
🔹 2. Recommend API
POST /recommend

Body:

{
  "input": "audit data"
}
🔹 3. Generate Report API (Main Feature)
POST /generate-report

Body:

{
  "input": "audit data"
}
🧠 Features
AI-powered analysis

Structured JSON responses

Modular Flask architecture

Prompt-based AI processing

✅ Status
APIs working ✔️

Tested using Postman ✔️

Code pushed to GitHub ✔️

👨‍💻 Author
Thejaswini k

