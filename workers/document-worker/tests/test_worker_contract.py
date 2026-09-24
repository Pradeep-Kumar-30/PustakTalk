from worker.jobs.generate_embeddings import generate_embeddings


class FakeEmbeddings:
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [[float(len(text))] for text in texts]


def test_empty_chunk_batch_does_not_embed() -> None:
    assert generate_embeddings([], FakeEmbeddings()) == []
