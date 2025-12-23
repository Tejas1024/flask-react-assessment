import uuid
from datetime import datetime
from typing import List, Optional
from modules.comment.types import (
    Comment,
    CreateCommentParams,
    UpdateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetCommentsByTaskParams,
)

# Mock in-memory storage for comments (in production, use a database)
comments_db: dict = {}

class CommentService:
    @staticmethod
    def create_comment(params: CreateCommentParams) -> Comment:
        """Create a new comment"""
        comment_id = str(uuid.uuid4())
        now = datetime.utcnow()
        comment = Comment(
            id=comment_id,
            task_id=params.task_id,
            account_id=params.account_id,
            content=params.content,
            created_at=now,
            updated_at=None,
        )
        comments_db[comment_id] = comment
        return comment

    @staticmethod
    def get_comment(params: GetCommentParams) -> Optional[Comment]:
        """Retrieve a specific comment"""
        for comment_id, comment in comments_db.items():
            if (
                comment.id == params.comment_id
                and comment.task_id == params.task_id
                and comment.account_id == params.account_id
            ):
                return comment
        return None

    @staticmethod
    def update_comment(params: UpdateCommentParams) -> Optional[Comment]:
        """Update an existing comment"""
        comment = CommentService.get_comment(
            GetCommentParams(
                comment_id=params.comment_id,
                task_id=params.task_id,
                account_id=params.account_id,
            )
        )
        if comment:
            updated_comment = Comment(
                id=comment.id,
                task_id=comment.task_id,
                account_id=comment.account_id,
                content=params.content,
                created_at=comment.created_at,
                updated_at=datetime.utcnow(),
            )
            comments_db[comment.id] = updated_comment
            return updated_comment
        return None

    @staticmethod
    def delete_comment(params: DeleteCommentParams) -> bool:
        """Delete a comment"""
        comment = CommentService.get_comment(
            GetCommentParams(
                comment_id=params.comment_id,
                task_id=params.task_id,
                account_id=params.account_id,
            )
        )
        if comment:
            del comments_db[comment.id]
            return True
        return False

    @staticmethod
    def get_comments_by_task(params: GetCommentsByTaskParams) -> List[Comment]:
        """Get all comments for a specific task"""
        task_comments = [
            comment
            for comment in comments_db.values()
            if comment.task_id == params.task_id
            and comment.account_id == params.account_id
        ]
        return task_comments
