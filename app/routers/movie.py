from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
# from ..utils import config, conn, models, oAuth 
from sqlalchemy.orm import Session
from utils.conn import get_db, engine
from schemas.movie import movieBase, movieEdit
from utils.models import Movie
from utils import models
from utils.oAuth import get_current_user



router   = APIRouter(
    prefix="/movie",
    tags=["Movie"]
)


# View a movie added (public access)
# Add a movie (authenticated access)
# View all movies (public access)
# Edit a movie (only by the user who listed it)
# Delete a movie (only by the user who listed it)


@router.get("/")
def view_all_movies(db: Session = Depends(get_db)):
    movie = db.query(models.Movie).all()
    return {"Movie Table": movie}


@router.get("/{movie_id}")
def view_one_movie(id: int, db: Session = Depends(get_db)):
    get_one_movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    
    if not get_one_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Movie not found")
    return get_one_movie


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_movie(movie: movieBase, db: Session = Depends(get_db), current_user: int = Depends (get_current_user)):
    create_movie = models.Movie(user_id =current_user.id,  **movie.model_dump())
    db.add(create_movie)
    db.commit()
    db.refresh(create_movie)
    return {"Successfully added": create_movie}


@router.put("/{movie_id}")
def edit_movie(editMovie:movieEdit, id: int, db: Session = Depends(get_db), current_user: int = Depends (get_current_user)):
    edit = db.query(models.Movie).filter(models.Movie.id == id)
    updatedMovie = edit.first()
    
    if updatedMovie == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with the id: {id} was not found")
    
    # FOR AUTH
    if updatedMovie != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested action")
    updatedMovie.update(edit_movie.model_dump(), synchronize_session=False)
    
    edit.update(editMovie.model_dump(), synchronize_session = False)
    db.commit()
    return edit.first()


@router.delete("/{movie_id}")
def delete_one_movie(id: int, db:Session= Depends(get_db), current_user: int = Depends (get_current_user)):
    delete_movie = db.query(models.Movie).filter(models.Movie.id == id)
    
    deleted = delete_movie.first()
    if deleted == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail = f"The movie with id: {id} was not found")
    
    if deleted.user_id != current_user:
        raise HTTPException (status_code= status.HTTP_401_UNAUTHORIZED, detail= "Not authorized to perform the requested action ")
    
    
    delete_movie.delete(synchronize_session=False)
    db.commit()
    return Response (status_code=status.HTTP_204_NO_CONTENT)




    
    
    
    
    






