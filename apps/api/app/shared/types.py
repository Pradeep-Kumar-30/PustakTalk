from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ChunkEvidence:
    chunk_id: UUID
    document_id: UUID
    document_name: str
    physical_page: int
    logical_page: str | None
    text: str
    bbox: list[float] | None
    section: str | None
    score: float
    metadata: dict[str, Any]
