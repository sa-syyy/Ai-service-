import chromadb

class ChromaService:
    def __init__(self):
        # Create local database (stored in memory for now)
        self.client = chromadb.Client()

        # Create collection (like table)
        self.collection = self.client.get_or_create_collection(
            name="audit_logs"
        )

    def add_text(self, text, doc_id):
        self.collection.add(
            documents=[text],
            ids=[doc_id]
        )

    def query_text(self, text):
        results = self.collection.query(
            query_texts=[text],
            n_results=1
        )
        return results