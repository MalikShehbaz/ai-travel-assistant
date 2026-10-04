# AI Travel Operations Assistant

An AI-powered travel operations assistant built with Python, FastAPI, PostgreSQL, pgvector, and Gemini.

The assistant can answer customer questions using a company knowledge base, retrieve relevant information through semantic search, create customer leads through an LLM tool call, and persist conversation history.

## Features

- AI-powered customer chat
- FastAPI backend
- Gemini LLM integration
- Retrieval-Augmented Generation (RAG)
- PostgreSQL database
- pgvector semantic search
- Gemini embeddings
- Knowledge-base ingestion and chunking
- LLM function calling
- Customer lead creation
- Conversation history
- Simple web chat interface
- Alembic database migrations
- Dockerized application
- Basic automated tests

## Architecture

```mermaid
flowchart TD
    A[Customer] --> B[Chat UI]
    B --> C[FastAPI API]

    C --> D[Conversation Service]
    D --> E[AI Service]

    E --> F[Gemini LLM]
    E --> G[Search Service]

    G --> H[Gemini Embeddings]
    G --> I[(PostgreSQL + pgvector)]

    E --> J[Create Lead Tool]
    J --> I

    D --> I

    K[Knowledge Document] --> L[Ingestion Service]
    L --> M[Chunking]
    M --> H
    H --> I