# ADR 002: Qdrant for dense vectors

**Status:** Accepted

Qdrant provides a self-hosted vector service with payload filtering. PostgreSQL remains the authoritative source for chunks, page provenance, permissions, and citations; Qdrant is an index that can be rebuilt.

