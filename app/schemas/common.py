from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    errors: Optional[List[dict]] = None
    meta: Optional[PaginationMeta] = None
