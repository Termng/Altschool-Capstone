from pydantic import BaseModel, EmailStr, PastDatetime, conint
from typing import Optional

class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str
    

class GetUser(BaseModel):
    username:str
    email: str
    created_at: PastDatetime
    
    class Config:
        orm_mode = True  # Enable ORM mode to work with SQLAlchemy models

class Authenticate(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    
    class Config:
        orm_mode = True