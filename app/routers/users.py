from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import UserModel
from schema import UserPasswordSchema, UserBaseSchema, UserResponseSchema
from database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from utils import get_password_hash

router = APIRouter(
    tags=['Users']
)


@router.get("/", response_model=UserResponseSchema)
def get_users(db: Session = Depends(get_db)):
    try:
        users_query = db.query(UserModel).all()
        users: List[UserBaseSchema] = []
        for user in jsonable_encoder(users_query):
            users.append(UserBaseSchema(**user))
        
        return UserResponseSchema(
            message='Users fetched successfully',
            data=users
        )
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", response_model=UserResponseSchema)
def create_user(payload: UserPasswordSchema, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(payload.password)
    payload.password = hashed_password
    new_user = UserModel(**payload.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserResponseSchema(
            message="User created successfully",
            data=UserBaseSchema(**jsonable_encoder(new_user))
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=jsonable_encoder(error))
