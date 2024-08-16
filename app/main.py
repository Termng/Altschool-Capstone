from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from routers import movie, users, login, rating
from utils.conn import engine, Base, SessionLocal




app = FastAPI(
    title= "Movie Database - OPENAPI 4.5",
    description = "movie database using FastAPI & Postgres",
    # docs_url="/"
)

@app.get("/")
def home_page():
    return {"message": "This is Torah's application"}



Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:   
    try:
        conn = psycopg2.connect(host='localhost', database = 'movieDB' , user = 'postgres', password = 'Merciful16', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connection to Postgres was successful')
        break
    except Exception as error:
        print('connection failed')
        print("Error: ", error)
        time.sleep(4)


app.include_router(movie.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(rating.router)


