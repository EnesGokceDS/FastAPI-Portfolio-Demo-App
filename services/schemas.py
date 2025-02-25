# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class QueryLogResponse(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str
    timestamp: datetime

    class Config:
        orm_mode = True
