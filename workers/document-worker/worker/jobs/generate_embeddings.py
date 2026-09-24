from app.ai.embeddings.base import EmbeddingProvider
from app.document_processing.chunking.base import ChunkDraft


def generate_embeddings(
    chunks: list[ChunkDraft], provider: EmbeddingProvider
) -> list[list[float]]:
    return provider.embed_documents([chunk.text for chunk in chunks])
