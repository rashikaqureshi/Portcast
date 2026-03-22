Paragraph Processing API
A robust FastAPI application designed to fetch, store, and analyze text paragraphs. The system integrates with external APIs to provide keyword search capabilities and top-word dictionary definitions.

Quick Start (Docker)
To get the system running immediately with all dependencies:

Build and start the containers:

Bash
docker-compose up --build
Access the API:
The API will be available at http://localhost:8000.

Interactive Documentation:
Visit http://localhost:8000/docs to test the endpoints via Swagger UI.


System Architecture
Tech Stack
Framework: FastAPI (Asynchronous Python)

Database: SQLite (SQLAlchemy ORM) — Chosen for simplicity in this deliverable, but easily swappable for PostgreSQL via env vars.

AI Disclosure & Thought Process
To meet the requirements of the assignment, the following is a breakdown of AI usage:

AI-Assisted: * Initial FastAPI/SQLAlchemy boilerplate setup.

Regex patterns for clean word extraction in utils.py.

Basic pytest structure and TestClient initialization.

Self-Authored / Strategic Decisions:

Architecture: Implemented the Service Layer pattern to separate concerns.

Robustness: Added defensive error handling for external API failures and implemented the definition_cache to minimize network latency.

DevOps: Configured the docker-compose environment.
