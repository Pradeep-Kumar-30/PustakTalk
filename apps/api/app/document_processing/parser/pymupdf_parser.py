import re

import pymupdf

from app.document_processing.parser.base import ExtractedBlock, ExtractedPage, PdfParser


def text_quality_score(text: str) -> float:
    compact = re.sub(r"\s+", "", text)
    if not compact:
        return 0.0
    readable = sum(char.isalnum() or char in ".,;:!?()[]-" for char in compact)
    return readable / len(compact)


class PyMuPdfParser(PdfParser):
    def extract(self, source: bytes) -> list[ExtractedPage]:
        document = pymupdf.open(stream=source, filetype="pdf")
        try:
            pages: list[ExtractedPage] = []
            for index, page in enumerate(document):
                raw_blocks = page.get_text("blocks", sort=True)
                blocks = [
                    ExtractedBlock(text=block[4].strip(), bbox=[float(item) for item in block[:4]])
                    for block in raw_blocks
                    if block[4].strip()
                ]
                text = "\n\n".join(block.text for block in blocks)
                pages.append(
                    ExtractedPage(
                        physical_page=index + 1,
                        text=text,
                        blocks=blocks,
                        width=page.rect.width,
                        height=page.rect.height,
                        extraction_method="native",
                        text_quality_score=text_quality_score(text),
                    )
                )
            return pages
        finally:
            document.close()
