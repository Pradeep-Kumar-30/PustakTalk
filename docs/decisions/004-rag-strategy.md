# ADR 004: hybrid, provenance-first retrieval

**Status:** Accepted

Dense retrieval is combined with database lexical retrieval through reciprocal-rank fusion. Reranking is optional on constrained hardware. Each answer citation is created from retrieved database chunks, which makes it impossible for the LLM to assign a page by itself.

