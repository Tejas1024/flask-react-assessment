import pytest
from modules.comment.comment_service import CommentService, comments_db
from modules.comment.types import (
    CreateCommentParams,
    UpdateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetCommentsByTaskParams,
)


class TestCommentService:
    """Test suite for Comment CRUD operations"""

    def setup_method(self):
        """Clear the in-memory database before each test"""
        comments_db.clear()

    def test_create_comment(self):
        """Test creating a new comment"""
        params = CreateCommentParams(
            task_id="task_123",
            account_id="account_456",
            content="This is a test comment"
        )
        
        comment = CommentService.create_comment(params)
        
        assert comment.task_id == "task_123"
        assert comment.account_id == "account_456"
        assert comment.content == "This is a test comment"
        assert comment.created_at is not None
        assert comment.updated_at is None
        assert comment.id is not None
        assert len(comments_db) == 1

    def test_get_comment(self):
        """Test retrieving a specific comment"""
        # Create a comment first
        create_params = CreateCommentParams(
            task_id="task_123",
            account_id="account_456",
            content="Test comment"
        )
        created = CommentService.create_comment(create_params)
        
        # Retrieve it
        get_params = GetCommentParams(
            comment_id=created.id,
            task_id="task_123",
            account_id="account_456"
        )
        retrieved = CommentService.get_comment(get_params)
        
        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.content == "Test comment"

    def test_get_comment_not_found(self):
        """Test retrieving a non-existent comment"""
        params = GetCommentParams(
            comment_id="nonexistent_id",
            task_id="task_123",
            account_id="account_456"
        )
        comment = CommentService.get_comment(params)
        
        assert comment is None

    def test_get_comment_wrong_account(self):
        """Test that users can only retrieve their own comments"""
        # Create comment for account_456
        create_params = CreateCommentParams(
            task_id="task_123",
            account_id="account_456",
            content="Private comment"
        )
        created = CommentService.create_comment(create_params)
        
        # Try to retrieve with wrong account_id
        get_params = GetCommentParams(
            comment_id=created.id,
            task_id="task_123",
            account_id="account_789"  # Different account
        )
        retrieved = CommentService.get_comment(get_params)
        
        assert retrieved is None

    def test_update_comment(self):
        """Test updating an existing comment"""
        # Create comment
        create_params = CreateCommentParams(
            task_id="task_123",
            account_id="account_456",
            content="Original content"
        )
        created = CommentService.create_comment(create_params)
        
        # Update it
        update_params = UpdateCommentParams(
            comment_id=created.id,
            task_id="task_123",
            account_id="account_456",
            content="Updated content"
        )
        updated = CommentService.update_comment(update_params)
        
        assert updated is not None
        assert updated.id == created.id
        assert updated.content == "Updated content"
        assert updated.updated_at is not None
        assert updated.created_at == created.created_at

    def test_update_comment_not_found(self):
        """Test updating a non-existent comment"""
        params = UpdateCommentParams(
            comment_id="nonexistent_id",
            task_id="task_123",
            account_id="account_456",
            content="New content"
        )
        updated = CommentService.update_comment(params)
        
        assert updated is None

    def test_delete_comment(self):
        """Test deleting a comment"""
        # Create comment
        create_params = CreateCommentParams(
            task_id="task_123",
            account_id="account_456",
            content="Comment to delete"
        )
        created = CommentService.create_comment(create_params)
        assert len(comments_db) == 1
        
        # Delete it
        delete_params = DeleteCommentParams(
            comment_id=created.id,
            task_id="task_123",
            account_id="account_456"
        )
        result = CommentService.delete_comment(delete_params)
        
        assert result is True
        assert len(comments_db) == 0

    def test_delete_comment_not_found(self):
        """Test deleting a non-existent comment"""
        params = DeleteCommentParams(
            comment_id="nonexistent_id",
            task_id="task_123",
            account_id="account_456"
        )
        result = CommentService.delete_comment(params)
        
        assert result is False

    def test_get_comments_by_task(self):
        """Test retrieving all comments for a task"""
        # Create multiple comments for same task
        for i in range(3):
            params = CreateCommentParams(
                task_id="task_123",
                account_id="account_456",
                content=f"Comment {i}"
            )
            CommentService.create_comment(params)
        
        # Create comment for different task
        other_params = CreateCommentParams(
            task_id="task_999",
            account_id="account_456",
            content="Other task comment"
        )
        CommentService.create_comment(other_params)
        
        # Get comments for task_123
        get_params = GetCommentsByTaskParams(
            task_id="task_123",
            account_id="account_456"
        )
        comments = CommentService.get_comments_by_task(get_params)
        
        assert len(comments) == 3
        assert all(c.task_id == "task_123" for c in comments)

    def test_get_comments_by_task_empty(self):
        """Test retrieving comments for a task with no comments"""
        params = GetCommentsByTaskParams(
            task_id="task_999",
            account_id="account_456"
        )
        comments = CommentService.get_comments_by_task(params)
        
        assert len(comments) == 0
        assert comments == []

    def test_get_comments_by_task_account_isolation(self):
        """Test that users only see their own comments"""
        # Create comments for account_456
        for i in range(2):
            params = CreateCommentParams(
                task_id="task_123",
                account_id="account_456",
                content=f"User 1 comment {i}"
            )
            CommentService.create_comment(params)
        
        # Create comments for account_789
        for i in range(3):
            params = CreateCommentParams(
                task_id="task_123",
                account_id="account_789",
                content=f"User 2 comment {i}"
            )
            CommentService.create_comment(params)
        
        # Get comments for account_456
        get_params = GetCommentsByTaskParams(
            task_id="task_123",
            account_id="account_456"
        )
        comments = CommentService.get_comments_by_task(get_params)
        
        assert len(comments) == 2
        assert all(c.account_id == "account_456" for c in comments)
