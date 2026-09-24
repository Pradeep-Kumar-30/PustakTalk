from app.shared.types import ChunkEvidence


class PageLocator:
    def answer(self, topic: str, evidence: list[ChunkEvidence]) -> str:
        if not evidence:
            return "I couldn't find sufficient evidence for this topic in the uploaded documents."
        pages: list[str] = []
        seen: set[tuple[str, int]] = set()
        for item in evidence:
            key = (item.document_name, item.physical_page)
            if key in seen:
                continue
            seen.add(key)
            section = f" — {item.section}" if item.section else ""
            pages.append(f"{item.document_name} — page {item.physical_page}{section}")
        return f"{topic} appears in:\n" + "\n".join(f"• {page}" for page in pages[:5])
