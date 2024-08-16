from pydantic import BaseModel
from typing import List

class movieBase(BaseModel):
    title: str
    synopsis: str
    release_year: int
    genre: List [str]
    duration: int
    is_g_rated: bool = True
    
    # class Config:
    #     orm_mode = True
    
    

class movieEdit(BaseModel):
    title: str
    synopsis: str
    release_year: int
    genre: List [str]
    duration: int
    is_g_rated: bool = True