from fastapi import Response, HTTPException, APIRouter, Depends, status
# from ..import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils import config, conn, helper, models, oAuth
from utils.conn import engine, get_db


router = APIRouter(tags=['Auth'])

@router.post("/login")
def login_user(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #fastapi comes with an inbuilt package for handling security (OAuth2PasswordRequestForm) 
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()   #make sure to pass username into this or it won't work
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    if not helper.validate_user(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')
    
    # this configures the jwt token
    access_token = oAuth.create_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}