# RAG API

FastAPI backend exposing the RAG catalog as a REST API.

## Endpoint
`POST /ask` — ask a question about the catalog

## Stack
- FastAPI
- LangChain
- ChromaDB
- Anthropic API

## Setup
```bash
pip install fastapi uvicorn langchain langchain-anthropic langchain-chroma sentence-transformers
uvicorn main:app --reload
```