from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.document_processing.parser.base import ExtractedPage


@dataclass(frozen=True, slots=True)
class ChunkDraft:
    physical_page: int
    logical_page: str | None
    chunk_key: str
    text: str
    heading: str | None
    section: str | None
    bbox: list[float] | None
    token_count: int
    extraction_method: str


class Chunker(ABC):
    @abstractmethod
    def chunk(self, pages: list[ExtractedPage]) -> list[ChunkDraft]: ...
