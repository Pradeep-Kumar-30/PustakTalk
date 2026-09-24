from dataclasses import dataclass

from app.document_processing.chunking.base import ChunkDraft
from app.document_processing.chunking.structure_aware import StructureAwareChunker
from app.document_processing.metadata.page_mapper import infer_logical_page
from app.document_processing.parser.base import ExtractedPage
from app.document_processing.parser.ocr_parser import TesseractOcrParser
from app.document_processing.parser.pymupdf_parser import PyMuPdfParser


@dataclass(frozen=True, slots=True)
class ProcessedDocument:
    pages: list[ExtractedPage]
    chunks: list[ChunkDraft]


class DocumentProcessingPipeline:
    def __init__(self, chunk_size_tokens: int, chunk_overlap_tokens: int) -> None:
        self._chunker = StructureAwareChunker(chunk_size_tokens, chunk_overlap_tokens)

    def process(self, source: bytes) -> ProcessedDocument:
        pages = PyMuPdfParser().extract(source)
        pages = TesseractOcrParser().enrich_low_quality_pages(source, pages)
        chunks = [
            draft.__class__(
                physical_page=draft.physical_page,
                logical_page=infer_logical_page(pages[draft.physical_page - 1]),
                chunk_key=draft.chunk_key,
                text=draft.text,
                heading=draft.heading,
                section=draft.section,
                bbox=draft.bbox,
                token_count=draft.token_count,
                extraction_method=draft.extraction_method,
            )
            for draft in self._chunker.chunk(pages)
        ]
        return ProcessedDocument(pages=pages, chunks=chunks)
