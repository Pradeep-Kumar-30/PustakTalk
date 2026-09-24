from uuid import uuid4

from app.ai.rag.citation_validator import validate_citations
from app.shared.types import ChunkEvidence


def test_validator_removes_duplicate_chunk_citations() -> None:
    document_id, chunk_id = uuid4(), uuid4()
    evidence = ChunkEvidence(
        chunk_id, document_id, "cn.pdf", 37, "25", "Slow Start", None, None, 1.0, {}
    )
    assert validate_citations([evidence, evidence]) == [evidence]
