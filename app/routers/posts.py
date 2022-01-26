from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from models import Posts
from oauth2 import get_current_user
from schema import PostErrorSchema, PostResponseSchema, PostSchema
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Posts']
)

@router.get('/', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    posts = db.query(
        Posts
    ).filter(
        Posts.is_published == True,
        Posts.is_deleted == False
    ).all()
    print(jsonable_encoder(get_current_user))
    response = PostResponseSchema(
        message="Posts fetched successfully",
        data=posts
    )
    return response


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
def get_posts_by_id(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    post = db.query(
        Posts
    ).filter(
        Posts.id == id,
        Posts.is_published == True,
        Posts.is_deleted == False
    ).first()

    if not post:
        response = PostErrorSchema(
            message="Requested post not found",
            error=post
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    response = PostResponseSchema(
        message="Post fetched successfully",
        data=post
    )
    return response


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostResponseSchema)
def create_post(payload: PostSchema, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    new_post = Posts(**payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    response = PostResponseSchema(
        message="Post created successfully",
        data=new_post
    )
    return response


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
def update_post(id: int, payload: PostSchema, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    payload.id = id
    update_query = db.query(
        Posts
    ).filter(
        Posts.id == id,
        Posts.is_published == True,
        Posts.is_deleted == False
    )
    post = update_query.first()

    if post == None:
        response = PostErrorSchema(
            message="Requested post not found",
            error=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )

    try:
        update_query.update(payload.dict(), synchronize_session=False)
        db.commit()
        response = PostResponseSchema(
            message="Post updated successfully",
            data=update_query.first()
        )
        return response
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=jsonable_encoder(error))


@router.delete('/{id}', status_code=status.HTTP_200_OK, response_model=PostResponseSchema)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(get_current_user)):
    deleted_post = db.query(
        Posts
    ).filter(
        Posts.id == id,
        Posts.is_published == True,
        Posts.is_deleted == False
    )
    if deleted_post.first() == None:
        response = PostErrorSchema(
            message="Requested post not found",
            error=None
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=response.dict()
        )
    deleted_post.update({Posts.is_deleted: True},
                        synchronize_session=False)
    db.commit()

    response = PostResponseSchema(
        message="Post deleted successfully",
        data=None
    )
    return response
