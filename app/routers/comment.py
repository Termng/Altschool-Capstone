
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from utils.conn import get_db
from utils.models import Comment
from schemas.comments import CommentCreate, CommentRead
from utils.oAuth import get_current_user

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_comment = Comment(**comment.dict(), user_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/movie/{movie_id}", response_model=List[CommentRead])
def get_comments_for_movie(movie_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.movie_id == movie_id).all()
    return comments

@router.post("/{comment_id}/reply", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def reply_to_comment(comment_id: int, reply: CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    parent_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if parent_comment is None:
        raise HTTPException(status_code=404, detail="Parent comment not found")
    db_reply = Comment(**reply.dict(), parent_id=comment_id, user_id=current_user.id)
    db.add(db_reply)
    db.commit()
    db.refresh(db_reply)
    return db_reply
