from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from schema import ErrorBaseSchema, ResponseBaseSchema


class PostBaseSchema(BaseModel):
    title: str
    content: str
    is_published: bool = True

class PostSchema(PostBaseSchema):
    id: Optional[int]
    created_at: Optional[datetime] = datetime.now().astimezone()
    updated_at: Optional[datetime] = datetime.now().astimezone()

    class Config():
        orm_mode = True

class PostResponseSchema(ResponseBaseSchema[PostSchema]):
    pass

class PostErrorSchema(ErrorBaseSchema[PostSchema]):
    pass