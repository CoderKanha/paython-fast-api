from fastapi import Depends, FastAPI, status, HTTPException
from psycopg2.extras import RealDictCursor
from database import engine, get_db
from sqlalchemy.orm import Session
import time
import psycopg2
import schemas
import models

models.Base.metadata.create_all(bind=engine)

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


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get('/posts', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(
        models.Posts
    ).filter(
        models.Posts.is_published == True,
        models.Posts.is_deleted == False
    ).all()
    response = schemas.PostResponse(
        message="Posts fetched successfully",
        data=posts
    )
    return response


@app.get('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(
        models.Posts
    ).filter(
        models.Posts.id == id,
        models.Posts.is_published == True,
        models.Posts.is_deleted == False
    ).first()

    if not post:
        response = schemas.PostError(
            message="Requested post not found",
            error=post
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    response = schemas.PostResponse(
        message="Post fetched successfully",
        data=post
    )
    return response


@app.post('/post', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.Posts, db: Session = Depends(get_db)):
    new_post = models.Posts(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    response = schemas.PostResponse(
        message="Post created successfully",
        data=new_post
    )
    return response


@app.put('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, payload: schemas.Posts, db: Session = Depends(get_db)):
    payload.id = id
    update_query = db.query(
        models.Posts
    ).filter(
        models.Posts.id == id,
        models.Posts.is_published == True,
        models.Posts.is_deleted == False
    )
    post = update_query.first()

    if post == None:
        response = schemas.PostError(
            message="Requested post not found",
            error=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )

    try:
        update_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        response = schemas.PostResponse(
            message="Post updated successfully",
            data=post
        )
        return response
    except Exception as error:
        print(error)
        response = schemas.PostError(
            message="Something went wrong",
            error=None
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response.dict())


@app.delete('/post/{id}', status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(
        models.Posts
    ).filter(
        models.Posts.id == id,
        models.Posts.is_published == True,
        models.Posts.is_deleted == False
    )
    if deleted_post.first() == None:
        response = schemas.PostError(
            message="Requested post not found",
            error=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    deleted_post.update({models.Posts.is_deleted: True},
                        synchronize_session=False)
    db.commit()

    response = schemas.PostResponse(
        message="Post deleted successfully",
        data=None
    )
    return response
