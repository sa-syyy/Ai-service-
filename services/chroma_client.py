import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.get_or_create_collection(name="audit_docs")
model = SentenceTransformer('all-MiniLM-L6-v2')

def query_docs(query):
    if not query:   # ✅ prevent crash
        return []

    embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=3)

    return results.get("documents", [[]])[0]