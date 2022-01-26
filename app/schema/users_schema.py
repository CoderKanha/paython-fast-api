from datetime import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, EmailStr

from schema import ResponseBaseSchema

T = TypeVar('T')
class UserBaseSchema(BaseModel):
    id: Optional[int]
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    created_at: Optional[datetime] = datetime.now().astimezone()
    updated_at: Optional[datetime] = datetime.now().astimezone()

    class Config():
        orm_mode = True

class UserPasswordSchema(UserBaseSchema):
    password: str


class UserResponseSchema(ResponseBaseSchema[UserBaseSchema]):
    pass
