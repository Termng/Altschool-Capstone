from fastapi import Response, HTTPException, APIRouter, Depends, status, Form
from typing import List, Optional
from sqlalchemy.orm import Session
from utils.conn import get_db, engine
from utils import models
from utils.oAuth import get_current_user
from schemas.rating import Rate, Rating


router = APIRouter(
    prefix="/ratings", 
    tags= ["Rating"]
)


@router.post("/")
def rate_movie(movie_id: int = Form(...), rating: Rate = Form(...), db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    my_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if not my_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    new_rating = models.Rating(user_id=current_user, movie_id=movie_id, rate=rating.value)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    
    return {"message": "Rated", "data": new_rating}