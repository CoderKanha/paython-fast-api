from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class ResponseBase(BaseModel):
    api_version: int = 1
    message: str

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True

class Posts(PostBase):
    id: Optional[int]
    # is_deleted: bool = False
    created_at: Optional[datetime] = datetime.now().astimezone()
    updated_at: Optional[datetime] = datetime.now().astimezone()

    class Config():
        orm_mode = True

class PostResponse(ResponseBase):
    data: Posts | List[Posts] | None

class PostError(ResponseBase):
    error: object | None