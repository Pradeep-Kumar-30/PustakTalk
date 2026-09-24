from sentence_transformers import SentenceTransformer

from app.ai.embeddings.base import EmbeddingProvider


class LocalEmbeddingProvider(EmbeddingProvider):
    """Loads a multilingual SentenceTransformer once per worker process."""

    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._model.encode(
            [f"passage: {text}" for text in texts], normalize_embeddings=True
        )
        return vectors.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self._model.encode(f"query: {text}", normalize_embeddings=True).tolist()
