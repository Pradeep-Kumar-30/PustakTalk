# ADR 001: modular monorepo

**Status:** Accepted

Web, API, worker, contracts, infrastructure, evaluation, and end-to-end tests share a repository while remaining independently buildable. This keeps API contracts and deploy configuration visible without coupling UI code to Python services.

