import os
import requests   # ✅ THIS LINE IS REQUIRED
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_groq(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
               "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5
            }
        )

        data = response.json()

        print("FULL RESPONSE:", data)  

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        else:
            return f"API Error: {data}"

    except Exception as e:
        return f"Error: {str(e)}"