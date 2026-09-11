from functools import lru_cache

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model only once per app process."""
    return SentenceTransformer("all-MiniLM-L6-v2")


class ResumeVectorStore:

    def __init__(self):
        # Reuse the same embedding model instead of loading it repeatedly.
        self.model = get_embedding_model()

        self.index = None
        self.chunks = []

    def create_chunks(self, text, chunk_size=500):
        """
        Split resume text into smaller chunks.
        """
        words = text.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)

        return chunks

    def create_index(self, text):
        """
        Convert resume chunks into embeddings
        and store them in a FAISS index.
        """
        self.chunks = self.create_chunks(text)

        embeddings = self.model.encode(
            self.chunks,
            show_progress_bar=False
        )
        embeddings = np.asarray(embeddings, dtype="float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query, top_k=3):
        """
        Convert the user query into an embedding
        and retrieve the most relevant resume chunks.
        """
        query_embedding = self.model.encode(
            [query],
            show_progress_bar=False
        )
        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        top_k = min(top_k, len(self.chunks))

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for i in indices[0]:
            results.append(self.chunks[i])

        return results
