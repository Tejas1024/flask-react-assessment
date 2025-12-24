import json
import unittest
from typing import Tuple

from server import app
from modules.account.account_service import AccountService
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import CreateAccountByUsernameAndPasswordParams, Account
from modules.logger.logger_manager import LoggerManager
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.rest_api.comment_rest_api_server import CommentRestApiServer
from modules.comment.comment_service import CommentService
from modules.comment.types import CreateCommentParams, Comment
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams, Task


class BaseTestComment(unittest.TestCase):
    ACCESS_TOKEN_URL = "http://127.0.0.1:8080/api/access-tokens"
    HEADERS = {"Content-Type": "application/json"}

    DEFAULT_USERNAME = "testuser@example.com"
    DEFAULT_PASSWORD = "testpassword"
    DEFAULT_FIRST_NAME = "Test"
    DEFAULT_LAST_NAME = "User"
    DEFAULT_TASK_TITLE = "Test Task"
    DEFAULT_TASK_DESCRIPTION = "Test Description"
    DEFAULT_COMMENT_CONTENT = "Test Comment"

    def setUp(self) -> None:
        LoggerManager.mount_logger()
        CommentRestApiServer.create()

    def tearDown(self) -> None:
        CommentRepository.collection().delete_many({})
        TaskRepository.collection().delete_many({})
        AccountRepository.collection().delete_many({})

    def create_test_account(
        self, username: str = None, password: str = None
    ) -> Account:
        return AccountService.create_account_by_username_and_password(
            params=CreateAccountByUsernameAndPasswordParams(
                username=username or self.DEFAULT_USERNAME,
                password=password or self.DEFAULT_PASSWORD,
                first_name=self.DEFAULT_FIRST_NAME,
                last_name=self.DEFAULT_LAST_NAME,
            )
        )

    def get_access_token(self, username: str = None, password: str = None) -> str:
        with app.test_client() as client:
            response = client.post(
                self.ACCESS_TOKEN_URL,
                headers=self.HEADERS,
                data=json.dumps(
                    {
                        "username": username or self.DEFAULT_USERNAME,
                        "password": password or self.DEFAULT_PASSWORD,
                    }
                ),
            )
            return response.json.get("token")

    def create_test_task(self, account_id: str) -> Task:
        return TaskService.create_task(
            params=CreateTaskParams(
                account_id=account_id,
                title=self.DEFAULT_TASK_TITLE,
                description=self.DEFAULT_TASK_DESCRIPTION,
            )
        )

    def create_test_comment(self, account_id: str, task_id: str, content: str = None) -> Comment:
        return CommentService.create_comment(
            params=CreateCommentParams(
                task_id=task_id,
                account_id=account_id,
                content=content or self.DEFAULT_COMMENT_CONTENT,
            )
        )

    def setup_account_and_task(self) -> Tuple[Account, str, Task]:
        """Helper to create account, get token, and create task"""
        account = self.create_test_account()
        token = self.get_access_token()
        task = self.create_test_task(account.id)
        return account, token, task

    def make_authenticated_request(
        self, method: str, account_id: str, token: str, task_id: str, comment_id: str = None, data: dict = None
    ):
        if comment_id:
            url = f"http://127.0.0.1:8080/api/accounts/{account_id}/tasks/{task_id}/comments/{comment_id}"
        else:
            url = f"http://127.0.0.1:8080/api/accounts/{account_id}/tasks/{task_id}/comments"

        headers = {**self.HEADERS, "Authorization": f"Bearer {token}"}

        with app.test_client() as client:
            if method.upper() == "GET":
                return client.get(url, headers={"Authorization": f"Bearer {token}"})
            elif method.upper() == "POST":
                return client.post(url, headers=headers, data=json.dumps(data) if data else None)
            elif method.upper() == "PATCH":
                return client.patch(url, headers=headers, data=json.dumps(data) if data else None)
            elif method.upper() == "DELETE":
                return client.delete(url, headers={"Authorization": f"Bearer {token}"})
