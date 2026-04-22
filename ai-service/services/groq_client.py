import os
import time
import logging
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("API key not found!")

        self.client = Groq(api_key=api_key)

    def generate_response(self, user_input):
        retries = 3

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "user", "content": user_input}
                    ]
                )

                return response.choices[0].message.content

            except Exception as e:
                logging.error(f"Error: {e}")
                time.sleep(2)

        return "Error: Failed after retries"