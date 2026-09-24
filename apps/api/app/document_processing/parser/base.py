from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtractedBlock:
    text: str
    bbox: list[float]


@dataclass(frozen=True, slots=True)
class ExtractedPage:
    physical_page: int
    text: str
    blocks: list[ExtractedBlock]
    width: float
    height: float
    extraction_method: str
    text_quality_score: float


class PdfParser(ABC):
    @abstractmethod
    def extract(self, source: bytes) -> list[ExtractedPage]: ...
