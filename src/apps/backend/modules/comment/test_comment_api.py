import json
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
    
    def test_get_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Test comment")
        
        response = self.make_authenticated_request(
            "GET", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 200
        assert response.json['id'] == comment.id
    
    def test_update_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "Original")
        update_data = {"content": "Updated"}
        
        response = self.make_authenticated_request(
            "PATCH", account.id, token, task.id, comment_id=comment.id, data=update_data
        )
        
        assert response.status_code == 200
        assert response.json['content'] == "Updated"
    
    def test_delete_comment_success(self):
        account, token, task = self.setup_account_and_task()
        comment = self.create_test_comment(account.id, task.id, "To delete")
        
        response = self.make_authenticated_request(
            "DELETE", account.id, token, task.id, comment_id=comment.id
        )
        
        assert response.status_code == 204