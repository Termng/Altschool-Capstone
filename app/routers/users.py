from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from utils.conn import get_db, engine
from schemas.movie import movieBase, movieEdit
from schemas.users import GetUser, CreateUser
from utils.models import Movie, User
from utils import models, helper



router = APIRouter(
    prefix="/user",
    tags=["User"]
)



# Create A user
# Login
# Get A user


@router.get("/", response_model = List[ GetUser])
def get_user( db: Session = Depends(get_db)):
    get_all_users = db.query(models.User).all()
    return get_all_users


@router.post("/")
def create_user(new_user: CreateUser, db:Session = Depends(get_db)):
    hashed_password = helper.hash(new_user.password) #this hashes the password
    new_user.password= hashed_password #this assigns the users password to a hashing function
    newUser = models.User(**new_user.model_dump()) #stores the pydantic model to a variable and maps it to the users table
    db.add(newUser) 
    db.commit()
    db.refresh(newUser)
    return newUser


