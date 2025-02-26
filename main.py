# main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers.query import router as query_router
from routers import auth  # our auth routes
from services.database import SessionLocal, engine
from services.models import User, Base
from routers.auth import get_password_hash
import openai, os
from services.llm import router as llm

app = FastAPI(title="RAG LLM FastAPI Demo")
Base.metadata.create_all(bind=engine)

# Mount static files (if any)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Include routers under prefixes
app.include_router(query_router, prefix="/api")
app.include_router(auth.router, prefix="/auth")

@app.post("/set_api_key")
async def set_api_key(data: dict):
    api_key = data.get("api_key")
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required.")
    openai.api_key = api_key
    return {"message": "API key set successfully."}

# (Optional) Create a default admin on startup if not exists
@app.on_event("startup")
def create_admin():
    db = SessionLocal()
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(username="admin", hashed_password=get_password_hash("admin123"), is_admin=True)
        db.add(admin)
        db.commit()
    db.close()

API_KEY=openai.api_key

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
