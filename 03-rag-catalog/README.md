# RAG Catalog

Ask questions about a product catalog using Retrieval Augmented Generation.

## How it works
1. Loads catalog from `catalog.txt`
2. Creates vector embeddings using HuggingFace
3. Stores in ChromaDB
4. On each question — finds relevant entries, passes to LLM

## Stack
- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Anthropic API