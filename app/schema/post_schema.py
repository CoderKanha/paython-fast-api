from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schema import UserBaseSchema

from app.schema import ErrorBaseSchema, ResponseBaseSchema


class PostBaseSchema(BaseModel):
    title: str = ''
    content: str = ''
    is_published: bool = True

class PostSchema(PostBaseSchema):
    id: Optional[int]
    created_at: datetime = datetime.now().astimezone()
    updated_at: datetime = datetime.now().astimezone()
    owner_id: Optional[int]
    owner: Optional[UserBaseSchema]

    class Config():
        orm_mode = True

class PostOutputSchema(PostBaseSchema):
    id: Optional[int]
    created_at: Optional[datetime] = datetime.now().astimezone()
    updated_at: Optional[datetime] = datetime.now().astimezone()
    owner_id: Optional[int]
    owner: UserBaseSchema

    class Config():
        orm_mode = True

class PostVoteSchema(BaseModel):
    Posts: PostSchema
    votes: int

    class Config():
        orm_mode = True

class PostVoteResponseSchema(ResponseBaseSchema[PostVoteSchema]):
    pass

class PostResponseSchema(ResponseBaseSchema[PostSchema]):
    pass

class PostErrorSchema(ErrorBaseSchema[PostSchema]):
    pass