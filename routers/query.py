# routers/query.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.vector_db import retrieve_context
from services.llm import generate_answer
from routers.auth import get_current_active_user, get_db
from services.models import QueryLog

router = APIRouter()

@router.get("/query")
def query_endpoint(q: str, current_user=Depends(get_current_active_user), db: Session = Depends(get_db)):
    """
    Retrieves context from the vector database and generates an answer.
    Logs the query and answer along with the user ID.
    """
    context = retrieve_context(q)
    if not context:
        raise HTTPException(status_code=404, detail="No relevant context found for your query.")
    
    answer = generate_answer(q, context)
    
    # Log the query and answer
    log_entry = QueryLog(user_id=current_user.id, question=q, answer=answer)
    db.add(log_entry)
    db.commit()
    
    return {"query": q, "answer": answer, "context": context}
