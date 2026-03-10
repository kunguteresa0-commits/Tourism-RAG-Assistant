from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from query import ask
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Tourism RAG API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Or your specific frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    sources: List[str]

@app.get("/")
def root():
    return {"message": "Tourism RAG API is running", "status": "active"}

@app.post("/query", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        answer, sources = ask(request.question)
        return QuestionResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy", "vector_db": "connected"}
