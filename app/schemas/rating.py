from enum import IntEnum
from pydantic import BaseModel

class Rate(IntEnum):
    Bad = 1
    Poor = 2
    Average = 3
    Good = 4
    Excellent = 5

class Rating(BaseModel):
    movie_ID : int
    rating: Rate
