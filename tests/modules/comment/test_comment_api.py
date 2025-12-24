from modules.comment.types import CommentErrorCode
from modules.authentication.types import AccessTokenErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    
    def test_create_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {"content": "Test comment"}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 201
        assert response.json['content'] == "Test comment"
        assert response.json['task_id'] == task.id
        assert response.json['account_id'] == account.id
    
    def test_create_comment_missing_content(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 400
        assert response.json['code'] == CommentErrorCode.BAD_REQUEST
    
    def test_get_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Test comment")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 200
        assert response.json['id'] == comment.id
        assert response.json['content'] == "Test comment"
    
    def test_get_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_update_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Original")
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=comment.id, data=update_data
        )
        
        assert response.status_code == 200
        assert response.json['content'] == "Updated"
        assert response.json['id'] == comment.id
    
    def test_update_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=fake_comment_id, data=update_data
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_delete_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "To delete")
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        assert get_response.status_code == 404
    
    def test_delete_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_get_task_comments_success(self):
        account, token, task = self.setup_account_and_task()
        
        # Create multiple comments
        self.create_test_comment(account.id, task.id, "Comment 1")
        self.create_test_comment(account.id, task.id, "Comment 2")
        self.create_test_comment(account.id, task.id, "Comment 3")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 3
    
    def test_get_task_comments_empty(self):
        account, token, task = self.setup_account_and_task()
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 0from modules.comment.types import CommentErrorCode
from modules.authentication.types import AccessTokenErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    
    def test_create_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {"content": "Test comment"}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 201
        assert response.json['content'] == "Test comment"
        assert response.json['task_id'] == task.id
        assert response.json['account_id'] == account.id
    
    def test_create_comment_missing_content(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 400
        assert response.json['code'] == CommentErrorCode.BAD_REQUEST
    
    def test_get_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Test comment")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 200
        assert response.json['id'] == comment.id
        assert response.json['content'] == "Test comment"
    
    def test_get_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_update_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Original")
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=comment.id, data=update_data
        )
        
        assert response.status_code == 200
        assert response.json['content'] == "Updated"
        assert response.json['id'] == comment.id
    
    def test_update_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=fake_comment_id, data=update_data
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_delete_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "To delete")
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        assert get_response.status_code == 404
    
    def test_delete_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_get_task_comments_success(self):
        account, token, task = self.setup_account_and_task()
        
        # Create multiple comments
        self.create_test_comment(account.id, task.id, "Comment 1")
        self.create_test_comment(account.id, task.id, "Comment 2")
        self.create_test_comment(account.id, task.id, "Comment 3")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 3
    
    def test_get_task_comments_empty(self):
        account, token, task = self.setup_account_and_task()
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 0from modules.comment.types import CommentErrorCode
from modules.authentication.types import AccessTokenErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    
    def test_create_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {"content": "Test comment"}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 201
        assert response.json['content'] == "Test comment"
        assert response.json['task_id'] == task.id
        assert response.json['account_id'] == account.id
    
    def test_create_comment_missing_content(self):
        account, token, task = self.setup_account_and_task()
        comment_data = {}
        
        response = self.make_authenticated_request(
            "POST", account.id, token, task.id, data=comment_data
        )
        
        assert response.status_code == 400
        assert response.json['code'] == CommentErrorCode.BAD_REQUEST
    
    def test_get_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Test comment")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 200
        assert response.json['id'] == comment.id
        assert response.json['content'] == "Test comment"
    
    def test_get_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_update_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Original")
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=comment.id, data=update_data
        )
        
        assert response.status_code == 200
        assert response.json['content'] == "Updated"
        assert response.json['id'] == comment.id
    
    def test_update_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=fake_comment_id, data=update_data
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_delete_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "To delete")
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        assert get_response.status_code == 404
    
    def test_delete_comment_not_found(self):
        account, token, task = self.setup_account_and_task()
        fake_comment_id = "507f1f77bcf86cd799439011"
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=fake_comment_id
        )
        
        assert response.status_code == 404
        assert response.json['code'] == CommentErrorCode.NOT_FOUND
    
    def test_get_task_comments_success(self):
        account, token, task = self.setup_account_and_task()
        
        # Create multiple comments
        self.create_test_comment(account.id, task.id, "Comment 1")
        self.create_test_comment(account.id, task.id, "Comment 2")
        self.create_test_comment(account.id, task.id, "Comment 3")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 3
    
    def test_get_task_comments_empty(self):
        account, token, task = self.setup_account_and_task()
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id
        )
        
        assert response.status_code == 200
        assert len(response.json) == 0
