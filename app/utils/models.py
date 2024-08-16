from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, PrimaryKeyConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .conn import Base

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    synopsis = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    duration = Column(String, nullable=False)  # Adjust this type if needed
    is_g_rated = Column(Boolean, server_default=text("True"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")
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
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    comment_text = Column(String, nullable=False)  # Changed 'comment' to 'comment_text'
    user = relationship("User")
    movie = relationship("Movie", back_populates="comments")
    __table_args__ = (PrimaryKeyConstraint('user_id', 'movie_id'),)

class Rating(Base):
    __tablename__ = 'rating'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id', ondelete='CASCADE'), nullable=False)
    rating_value = Column(Integer, nullable=False)  # Changed 'Rating' to 'rating_value'
    user = relationship("User")
    movie = relationship("Movie", back_populates="ratings")
    __table_args__ = (PrimaryKeyConstraint('user_id', 'movie_id'),)
