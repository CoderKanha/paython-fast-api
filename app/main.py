from fastapi import Depends, FastAPI, status, HTTPException
from psycopg2.extras import RealDictCursor
from database import engine, get_db
from sqlalchemy.orm import Session
from routers import users, posts
import time
import psycopg2
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

while True:
    try:
        print('Connecting to database...')
        conn = psycopg2.connect(
            host='localhost',
            database="fastapi",
            user="postgres",
            password="admin",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Connected to database successfully...')
        break
    except Exception as error:
        print('Failed to connect to database...')
        print('Error: ', error)
        time.sleep(5)


@app.get('/')
def root():
    return {"message": "Hello World"}
