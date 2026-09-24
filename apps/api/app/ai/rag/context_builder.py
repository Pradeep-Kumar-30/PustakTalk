from app.shared.types import ChunkEvidence


def build_context(evidence: list[ChunkEvidence], max_characters: int = 18_000) -> str:
    parts: list[str] = []
    remaining = max_characters
    for item in evidence:
        source = (
            f"[{item.document_name} | physical page {item.physical_page} | chunk {item.chunk_id}]"
        )
        text = item.text[: max(0, remaining - len(source) - 2)]
        if not text:
            break
        parts.append(f"{source}\n{text}")
        remaining -= len(source) + len(text) + 2
    return "\n\n".join(parts)
