from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .conn import Base


class Movie(Base):
    __tablename__ = "movie"
    id= Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    synopsis = Column(String, nullable= False)
    release_year= Column(Integer, nullable= False)
    genre= Column(String, nullable= False)
    duration= Column(String, nullable= False)
    is_g_rated = Column(Boolean, server_default='True', nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable= False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user= relationship("User")
    ratings = relationship("Rating", back_populates="movie")
    comments = relationship("Comment", back_populates="movie")
    
    
    


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


    

class Comment(Base):
    __tablename__= 'comment'

    id = Column(Integer, primary_key=True, index=True, nullable=False )
    text = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('Movie.id', ondelete='CASCADE'), primary_key=True)
    comment = Column(String, nullable= False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Comment", backref="parent", remote_side=[id])

    
class Rating(Base):
    __tablename__= 'rating'

    id = Column(Integer, primary_key=True, index=True, nullable=False )
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('Movie.id', ondelete='CASCADE'), primary_key=True)
    Rating = Column(Integer, nullable= False)

    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
    

    