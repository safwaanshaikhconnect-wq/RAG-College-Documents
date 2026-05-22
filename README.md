# College Doc Q&A — RAG System

A full-stack Retrieval-Augmented Generation (RAG) app that lets you chat with your college documents.

## Tech Stack
- **Frontend:** React + Vite
- **Backend:** FastAPI
- **Embeddings:** FastEmbed (bge-small-en-v1.5)
- **Vector DB:** ChromaDB
- **LLM:** Llama 3.1 via Groq API

## Features
- Upload any PDF and ask questions from it
- Answers grounded in your documents, not hallucinated
- Page-level source citation
- Clean chat UI

## Setup
1. Clone the repo
2. Add your `GROQ_API_KEY` to `backend/.env`
3. Run `pip install -r backend/requirements.txt`
4. Run `python backend/ingest.py` to ingest PDFs
5. Run `uvicorn main:app --reload` in `backend/`
6. Run `npm install && npm run dev` in `frontend/`
