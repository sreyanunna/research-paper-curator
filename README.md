# Research Paper Curator

A personal, from-scratch build of a production-grade RAG system that turns arXiv
papers into searchable, answerable knowledge. Rebuilt piece by piece (following
the Jam with AI's*[The Mother of AI Project](https://jamwithai.substack.com/p/the-infrastructure-that-powers-rag)*) to understand every component.
**Status: Week 1 — infrastructure complete.**

## What was built (Week 1)

A Docker Compose stack orchestrating containerized services on a shared private
network, each addressable by service name via Docker's internal DNS:

- **FastAPI** (`api`, built from a local `Dockerfile`) — async backend with a `/health` endpoint.
- **PostgreSQL** (`postgres:16-alpine`) — persistent metadata store (named volume).
- **OpenSearch** (`opensearchproject/opensearch:2.19.0`) — search engine (named volume; security disabled for local dev).
- **Ollama** (`ollama/ollama`) — local LLM runtime (named volume for models).

Each service was added one at a time to a minimal base and verified before the next.

## Tools & platforms

- **uv** — Python project & dependency management
- **Docker / Docker Compose** — containerization and orchestration
- **Git / GitHub** — version control
- **VS Code** — editor + integrated terminal
- **`.env`** — credentials/config, kept out of Git and images
- **Claude Opus 4.8** — step-by-step guidance and concept explanations

## Health checks

- `GET /health` → `{"status":"ok"}`
- `docker compose ps` → services report `(healthy)`
- `pg_isready` (Postgres), `_cluster/health` (OpenSearch), `ollama list` (Ollama)
- Internal networking verified from the `api` container (name resolution to `postgres`, `opensearch`, `ollama`)

## The five services and their purpose

- **FastAPI** — the API front door; receives requests and coordinates the other services.
- **PostgreSQL** — source of truth for structured paper metadata.
- **OpenSearch** — retrieval engine; ranks papers by relevance (BM25 + vectors).
- **Airflow** — orchestrates automated daily ingestion *(added in Week 2)*.
- **Ollama** — runs a local LLM to generate answers from retrieved papers *(used in Week 5)*.

## Mock data pipeline

To develop and test without depending on the live arXiv API, a **mock** source
stands in for it. The pipeline runs the *real* storage/index path using *fake*
input — only the source is mocked.

![Mock data pipeline](mock_data_pipeline_flow.png)

A local `sample_papers.json` (fake papers) is read by a **loader** function in
`src/`, which writes metadata to **PostgreSQL** and indexes searchable content
into **OpenSearch**. This proves the downstream plumbing end-to-end and stays
unchanged when the real arXiv fetcher replaces the JSON in Week 2. A
`notebooks/week1/mock_pipeline.ipynb` drives the loader step by step for
verification.

*Current progress:* the file → loader step is complete; the PostgreSQL and
OpenSearch writes are the next steps.
