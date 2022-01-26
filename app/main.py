from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from database import engine, Base
from routers import users, posts, oauth
import time
import psycopg2

Base.metadata.create_all(bind=engine)

app = FastAPI()

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


app.include_router(users.router, prefix="/user")
app.include_router(posts.router, prefix="/post")
app.include_router(oauth.router)


@app.get('/')
def root():
    return {"message": "Hello World"}
