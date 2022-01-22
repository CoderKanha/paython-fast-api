from random import randrange
from typing import List, Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


app = FastAPI()


class PostSchema(BaseModel):
    id: Optional[int]
    title: str
    content: str
    is_publish: bool = True
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
        "is_publish": True,
        "rating": 5
    },
    {
        "id": 2,
        "title": "Post 2 Title",
        "content": "Post 2 Content",
        "is_publish": True,
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
    response = ResponseSchema(
        message="Posts fetched successfully",
        data=my_posts
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
    payload.id = randrange(1, 1000000)
    my_posts.append(payload.dict())
    response = ResponseSchema(
        message="Post created successfully",
        data=payload
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
