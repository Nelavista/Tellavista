-- Runs once on first `docker compose up` for a fresh local database volume.
CREATE EXTENSION IF NOT EXISTS vector;   -- pgvector: RAG embeddings (audit §2.3, ADR-0001)
CREATE EXTENSION IF NOT EXISTS pg_trgm;  -- fuzzy/substring search
CREATE EXTENSION IF NOT EXISTS unaccent; -- accent-insensitive search
