from pydantic import BaseModel, EmailStr

from schema import ResponseBaseSchema


class UserBase(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(ResponseBaseSchema[UserBase]):
    pass
