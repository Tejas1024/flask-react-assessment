from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from modules.application.common.types import PaginationParams, SortParams

@dataclass(frozen=True)
class Comment:
    id: str
    task_id: str
    account_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

@dataclass(frozen=True)
class CreateCommentParams:
    task_id: str
    account_id: str
    content: str

@dataclass(frozen=True)
class UpdateCommentParams:
    comment_id: str
    task_id: str
    account_id: str
    content: str

@dataclass(frozen=True)
class DeleteCommentParams:
    comment_id: str
    task_id: str
    account_id: str

@dataclass(frozen=True)
class GetCommentParams:
    comment_id: str
    task_id: str
    account_id: str

@dataclass(frozen=True)
class GetCommentsByTaskParams:
    task_id: str
    account_id: str
    pagination_params: Optional[PaginationParams] = None
    sort_params: Optional[SortParams] = None
