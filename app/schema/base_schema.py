from pydantic import BaseModel
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar('T')
S = TypeVar('S')
class BaseSchema(BaseModel):
    api_version: int = 1
    message: str

    class Config():
        orm_mode = True

class ResponseBaseSchema(BaseSchema, Generic[T]):
    data: Any

class ErrorBaseSchema(BaseSchema, Generic[T]):
    error: Any