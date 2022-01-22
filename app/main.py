from random import randrange
import time
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


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


# cursor.execute("SELECT * FROM posts")
# records = cursor.fetchall()

# print('Records: ', records)


class PostSchema(BaseModel):
    id: Optional[int]
    title: str
    content: str
    is_published: bool = True
    rating: Optional[int] = None


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


def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index(id: int):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index


@app.get('/')
def root():
    return {"message": "Hello World"}


@app.get('/posts', status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute(""" SELECT * from posts ORDER BY id""")
    posts = cursor.fetchall()
    response = ResponseSchema(
        message="Posts fetched successfully",
        data=posts
    )
    return response


@app.get('/post/{id}', status_code=status.HTTP_200_OK)
def get_posts_by_id(id: int):
    post = find_post(id)
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
def create_post(payload: PostSchema):

    cursor.execute(
        """ INSERT INTO posts (title, content, is_published) VALUES (%s, %s, %s) RETURNING * """,
        (payload.title, payload.content, payload.is_published)
    )

    new_post = cursor.fetchone()
    conn.commit()
    response = ResponseSchema(
        message="Post created successfully",
        data=new_post
    )
    return response


@app.put('/post/{id}', status_code=status.HTTP_200_OK)
def update_post(id: int, payload: PostSchema):
    post_index = find_index(id)
    print(post_index)
    if post_index == None:
        response = ResponseSchema(
            message="Requested post not found",
            data=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    my_posts[post_index] = payload.dict()
    response = ResponseSchema(
        message="Post updated successfully",
        data=payload
    )
    return response


@app.delete('/post/{id}', status_code=status.HTTP_200_OK)
def delete_post(id: int):
    post_index = find_index(id)
    print(post_index)
    if post_index == None:
        response = ResponseSchema(
            message="Requested post not found",
            data=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    my_posts.pop(post_index)
    response = ResponseSchema(
        message="Post deleted successfully",
        data=None
    )
    return response
