from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from models import UserModel
from schema import UserPasswordSchema, UserBaseSchema
from database import get_db
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from utils import get_password_hash

router = APIRouter(
    prefix="/user"
)


@router.get("/", response_model=List[UserBaseSchema])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(UserModel).all()
        return users
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/", response_model=UserBaseSchema)
def create_user(payload: UserPasswordSchema, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(payload.password)
    payload.password = hashed_password
    new_user = UserModel(**payload.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=jsonable_encoder(error))
