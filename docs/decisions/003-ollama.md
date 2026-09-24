# ADR 003: Ollama for local LLM inference

**Status:** Accepted

Ollama's local `/api` endpoint works without a cloud key and exposes a stable local abstraction. Qwen3 is configured by environment rather than bundled into an image. The current host has no GPU and limited free RAM, so `.env.example` uses the 0.6B profile; move to 1.7B or 4B only after measuring memory and latency.

