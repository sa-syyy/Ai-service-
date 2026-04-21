import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

print("API KEY LOADED:", api_key is not None)
print("AI is ready. How can I assist you?")

client = Groq(api_key=api_key)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    print("AI:", response.choices[0].message.content)