from app.document_processing.parser.base import ExtractedPage
from app.document_processing.parser.ocr_parser import TesseractOcrParser
from app.document_processing.parser.pymupdf_parser import PyMuPdfParser


def extract_pages(source: bytes) -> list[ExtractedPage]:
    return TesseractOcrParser().enrich_low_quality_pages(
        source, PyMuPdfParser().extract(source)
    )
