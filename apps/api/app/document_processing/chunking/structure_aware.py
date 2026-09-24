import re

from app.document_processing.chunking.base import ChunkDraft, Chunker
from app.document_processing.parser.base import ExtractedPage

_HEADING = re.compile(r"^(?:\d+(?:\.\d+)*\s+)?[A-Z][A-Za-z0-9 ,:()/-]{2,100}$")
_TOKEN = re.compile(r"\S+")


class StructureAwareChunker(Chunker):
    """Keeps chunks inside a page and prefers paragraph/heading boundaries."""

    def __init__(self, size_tokens: int, overlap_tokens: int) -> None:
        self._size = size_tokens
        self._overlap = overlap_tokens

    def chunk(self, pages: list[ExtractedPage]) -> list[ChunkDraft]:
        drafts: list[ChunkDraft] = []
        current_heading: str | None = None
        for page in pages:
            paragraphs = [
                paragraph.strip()
                for paragraph in re.split(r"\n\s*\n", page.text)
                if paragraph.strip()
            ]
            buffer: list[str] = []
            token_count = 0
            sequence = 0
            for paragraph in paragraphs:
                if _HEADING.match(paragraph) and len(_TOKEN.findall(paragraph)) <= 14:
                    if buffer:
                        drafts.append(
                            self._draft(page, sequence, buffer, token_count, current_heading)
                        )
                        sequence += 1
                        buffer, token_count = [], 0
                    current_heading = paragraph
                    continue
                for unit in self._split_long_paragraph(paragraph):
                    unit_tokens = _TOKEN.findall(unit)
                    if buffer and token_count + len(unit_tokens) > self._size:
                        drafts.append(
                            self._draft(page, sequence, buffer, token_count, current_heading)
                        )
                        sequence += 1
                        overlap = _TOKEN.findall(" ".join(buffer))[-self._overlap :]
                        buffer, token_count = ([" ".join(overlap)] if overlap else []), len(overlap)
                    buffer.append(unit)
                    token_count += len(unit_tokens)
            if buffer:
                drafts.append(self._draft(page, sequence, buffer, token_count, current_heading))
        return drafts

    def _split_long_paragraph(self, paragraph: str) -> list[str]:
        sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", paragraph) if item.strip()]
        if not sentences:
            return []
        units: list[str] = []
        current: list[str] = []
        current_tokens = 0
        for sentence in sentences:
            sentence_tokens = _TOKEN.findall(sentence)
            if current and current_tokens + len(sentence_tokens) > self._size:
                units.append(" ".join(current))
                current, current_tokens = [], 0
            current.append(sentence)
            current_tokens += len(sentence_tokens)
        if current:
            units.append(" ".join(current))
        return units

    @staticmethod
    def _draft(
        page: ExtractedPage, sequence: int, parts: list[str], token_count: int, heading: str | None
    ) -> ChunkDraft:
        return ChunkDraft(
            physical_page=page.physical_page,
            logical_page=None,
            chunk_key=f"p{page.physical_page:04d}_c{sequence:03d}",
            text="\n\n".join(parts),
            heading=heading,
            section=heading,
            bbox=[0, 0, page.width, page.height],
            token_count=token_count,
            extraction_method=page.extraction_method,
        )
