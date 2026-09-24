import re

from app.document_processing.parser.base import ExtractedPage

_PRINTED_PAGE = re.compile(r"(?:^|\n)\s*(\d{1,4})\s*(?:$|\n)")


def infer_logical_page(page: ExtractedPage) -> str | None:
    """Conservative mapping: only record a printed page number when it is explicit."""
    matches = _PRINTED_PAGE.findall(page.text)
    return matches[-1] if matches else None
