from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from retriever import build_chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = build_chain()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: QueryRequest):
    answer = chain.invoke(request.question)
    return {"answer": answer}

@app.get("/health")
def health():
    return {"status": "ok"}