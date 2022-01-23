import datetime
from random import randrange
import time
from typing import List, Optional
from fastapi import Depends, FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import null
import models
from models import Posts
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

while True:
    try:
        print('Connecting to database...')
        conn = psycopg2.connect(host='localhost', database="fastapi",
                                user="postgres", password="admin", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Connected to database successfully...')
        break
    except Exception as error:
        print('Failed to connect to database...')
        print('Error: ', error)
        time.sleep(5)


class PostSchema(BaseModel):
    id: Optional[int]
    title: str
    content: str
    is_published: bool = True
    is_deleted: bool = False
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class ResponseSchema(BaseModel):
    api_version: int = 1
    message: str
    data: object


my_posts: List[PostSchema] = [
    {
        "id": 1,
        "title": "Post 1 Title",
        "content": "Post 1 Content",
        "is_published": True,
        "rating": 5
    },
    {
        "id": 2,
        "title": "Post 2 Title",
        "content": "Post 2 Content",
        "is_published": True,
        "rating": 4.3
    }
]


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get('/posts', status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * from posts WHERE NOT is_deleted ORDER BY id""")
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    response = ResponseSchema(
        message="Posts fetched successfully",
        data=posts
    )
    return response


@app.get('/post/{id}', status_code=status.HTTP_200_OK)
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE NOT is_deleted AND id = %s """, (str(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Posts).filter(models.Posts.id == id, models.Posts.is_deleted == False).first()

    if not post:
        response = ResponseSchema(
            message="Requested post not found",
            data=post
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    response = ResponseSchema(
        message="Post fetched successfully",
        data=post
    )
    return response


@app.post('/post', status_code=status.HTTP_201_CREATED)
def create_post(payload: PostSchema, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """ INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """,
    #     (payload.title, payload.content, payload.is_published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Posts(**payload.dict())
    db.add(new_post)
    db.commit()
    # To return the newly created post
    db.refresh(new_post)

    response = ResponseSchema(
        message="Post created successfully",
        data=new_post
    )
    return response


@app.put('/post/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, payload: PostSchema, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """ UPDATE posts SET title = %s, content = %s, is_published = %s WHERE NOT is_deleted AND id = %s RETURNING *""",
    #     (payload.title, payload.content, payload.is_published, id)
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    payload.id = id

    update_query = db.query(models.Posts).filter(models.Posts.id == id, models.Posts.is_deleted == False)
    post = update_query.first()

    if post == None:
        response = ResponseSchema(
            message="Requested post not found",
            data=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    
    try:
        update_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        response = ResponseSchema(
            message="Post updated successfully",
            data=update_query.first()
        )
        return response
    except Exception as error:
        response = ResponseSchema(
            message="Something went wrong"
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response.dict())


@app.delete('/post/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET is_deleted = true WHERE NOT is_deleted AND id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Posts).filter(models.Posts.id == id, models.Posts.is_deleted == False)
    if deleted_post.first() == None:
        response = ResponseSchema(
            message="Requested post not found",
            data=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    deleted_post.update({models.Posts.is_deleted: True} ,synchronize_session=False)
    db.commit()

    response = ResponseSchema(
        message="Post deleted successfully",
        data=null
    )
    return response
