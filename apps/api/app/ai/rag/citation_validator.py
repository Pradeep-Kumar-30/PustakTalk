from app.shared.types import ChunkEvidence


def validate_citations(evidence: list[ChunkEvidence]) -> list[ChunkEvidence]:
    """Citations originate solely from retrieved chunk metadata, never from generated prose."""
    unique: dict[tuple[str, int, str], ChunkEvidence] = {}
    for item in evidence:
        key = (str(item.document_id), item.physical_page, str(item.chunk_id))
        unique[key] = item
    return list(unique.values())
