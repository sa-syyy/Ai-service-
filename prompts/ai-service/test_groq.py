from services.groq_client import GroqClient

print("AI is ready. How can I assist you?")

client = GroqClient()

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Exiting...")
        break

    response = client.generate_response(user_input)
    print("AI:", response)