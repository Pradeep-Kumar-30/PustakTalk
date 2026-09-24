import io

import pymupdf
import pytesseract
from PIL import Image

from app.document_processing.parser.base import ExtractedBlock, ExtractedPage
from app.document_processing.parser.pymupdf_parser import text_quality_score


class TesseractOcrParser:
    """OCR only insufficient native pages; native text always takes precedence."""

    def enrich_low_quality_pages(
        self, source: bytes, pages: list[ExtractedPage], language: str = "eng+hin"
    ) -> list[ExtractedPage]:
        document = pymupdf.open(stream=source, filetype="pdf")
        try:
            enriched: list[ExtractedPage] = []
            for extracted in pages:
                if extracted.text_quality_score >= 0.45 and len(extracted.text.strip()) >= 40:
                    enriched.append(extracted)
                    continue
                page = document[extracted.physical_page - 1]
                image = Image.open(
                    io.BytesIO(page.get_pixmap(matrix=pymupdf.Matrix(2, 2)).tobytes("png"))
                )
                text = pytesseract.image_to_string(image, lang=language).strip()
                enriched.append(
                    ExtractedPage(
                        physical_page=extracted.physical_page,
                        text=text,
                        blocks=[
                            ExtractedBlock(
                                text=text, bbox=[0, 0, page.rect.width, page.rect.height]
                            )
                        ]
                        if text
                        else [],
                        width=page.rect.width,
                        height=page.rect.height,
                        extraction_method="ocr",
                        text_quality_score=text_quality_score(text),
                    )
                )
            return enriched
        finally:
            document.close()
