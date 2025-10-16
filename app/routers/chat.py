from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.rag import RagService
from pydantic import BaseModel
import logging

router = APIRouter()

class ChatRequest(BaseModel):
    session_id: str
    message: str

def get_rag_service(db: Session = Depends(get_db)):
    return RagService(db=db)

@router.post("/chat")
def chat(request: ChatRequest, rag_service: RagService = Depends(get_rag_service)):
    """
    Handles chat requests.
    """
    try:
        response = rag_service.process_query(request.message)
        return response
    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again later.")

