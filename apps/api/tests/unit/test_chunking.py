from app.document_processing.chunking.structure_aware import StructureAwareChunker
from app.document_processing.parser.base import ExtractedPage


def test_chunker_keeps_each_chunk_on_its_source_page() -> None:
    page = ExtractedPage(
        physical_page=7,
        text="Congestion Control\n\n" + "A sentence. " * 40,
        blocks=[],
        width=600,
        height=800,
        extraction_method="native",
        text_quality_score=1.0,
    )
    chunks = StructureAwareChunker(size_tokens=20, overlap_tokens=3).chunk([page])
    assert len(chunks) > 1
    assert {chunk.physical_page for chunk in chunks} == {7}
    assert all(chunk.chunk_key.startswith("p0007") for chunk in chunks)
