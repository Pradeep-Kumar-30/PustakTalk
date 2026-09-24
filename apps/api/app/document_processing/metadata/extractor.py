from dataclasses import dataclass

from app.document_processing.parser.base import ExtractedPage


@dataclass(frozen=True, slots=True)
class DocumentMetadata:
    page_count: int
    native_page_count: int
    ocr_page_count: int


def extract_document_metadata(pages: list[ExtractedPage]) -> DocumentMetadata:
    return DocumentMetadata(
        page_count=len(pages),
        native_page_count=sum(page.extraction_method == "native" for page in pages),
        ocr_page_count=sum(page.extraction_method == "ocr" for page in pages),
    )
