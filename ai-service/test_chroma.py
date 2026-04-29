from services.chroma_service import ChromaService

chroma = ChromaService()

# Add sample data
chroma.add_text("Unauthorized transaction detected", "1")
chroma.add_text("Payment failed due to network error", "2")

# Query similar
result = chroma.query_text("fraud transaction")

print(result)