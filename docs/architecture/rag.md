# RAG and citation architecture

Every page is retained as a `document_page`; every chunk retains its document ID, physical PDF page, optional printed logical page, text, extraction method, and bounding box. Physical pages are the source of truth. Printed page numbers are recorded only when a conservative mapper finds one explicitly.

```text
question → LangGraph intent route → dense + lexical retrieval → RRF fusion
         → document filter → local reranking → bounded context → local LLM
         → citation validation → groundedness signal
```

Page lookup bypasses generative page-number selection: it groups retrieved chunks by their stored physical pages. Chat citations are persisted from retrieved chunks, not parsed from model text. This is the core protection against fabricated pages.

The default embedding profile is `intfloat/multilingual-e5-small` for the current CPU-only development host. A larger server may use BGE-M3 after evaluation; its model card describes 1024-dimensional embeddings, 8,192-token inputs, multilingual support, and an MIT licence. Retrieval quality must be measured with `make eval` and a seeded corpus before making claims.

