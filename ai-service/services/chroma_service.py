import chromadb

class ChromaService:
    def __init__(self):
        # Create local database (in-memory for now)
        self.client = chromadb.Client()

        # Create collection (like a table)
        self.collection = self.client.get_or_create_collection(
            name="audit_logs"
        )

    # 🔹 Add text to DB
    def add_text(self, text, doc_id):
        self.collection.add(
            documents=[text],
            ids=[doc_id]
        )

    # 🔹 Old function (keep it for compatibility)
    def query_text(self, text):
        results = self.collection.query(
            query_texts=[text],
            n_results=1
        )
        return results

    # 🔥 NEW FUNCTION (Day 5)
    def query_with_docs(self, text):
        results = self.collection.query(
            query_texts=[text],
            n_results=3
        )

        return {
            "documents": results.get("documents", [[]])[0],
            "ids": results.get("ids", [[]])[0]
        }