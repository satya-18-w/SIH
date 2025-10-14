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

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handles chat requests.
    """
    try:
        rag_service = RagService(db=db)
        response = rag_service.process_query(request.message)
        return response
    except Exception as e:
        logging.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again later.")

