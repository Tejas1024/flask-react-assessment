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
cat > src/apps/frontend/components/tasks/TaskManager.css << 'EOF'
.task-manager {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.task-manager h1 {
  color: #333;
  margin-bottom: 30px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.add-task-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.add-task-form h2 {
  color: #495057;
  font-size: 18px;
  margin-bottom: 15px;
}

.add-task-form input,
.add-task-form textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
}

.add-task-form textarea {
  resize: vertical;
  min-height: 80px;
}

.add-task-form button {
  background-color: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.add-task-form button:hover {
  background-color: #218838;
}

.tasks-list h2 {
  color: #495057;
  margin-bottom: 20px;
  font-size: 18px;
}

.no-tasks {
  text-align: center;
  color: #6c757d;
  padding: 40px 20px;
  background: #f8f9fa;
  border-radius: 4px;
}

.tasks-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  margin-bottom: 15px;
  padding: 20px;
}

.view-task h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.view-task p {
  color: #6c757d;
  margin: 0 0 15px 0;
  font-size: 14px;
}

.edit-task input,
.edit-task textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: inherit;
  font-size: 14px;
}

.edit-task textarea {
  resize: vertical;
  min-height: 80px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn-edit, .btn-delete, .btn-save, .btn-cancel {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-edit {
  background-color: #007bff;
  color: white;
}

.btn-edit:hover {
  background-color: #0056b3;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.btn-delete:hover {
  background-color: #c82333;
}

.btn-save {
  background-color: #28a745;
  color: white;
}

.btn-save:hover {
  background-color: #218838;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background-color: #5a6268;
}
EOF
clear && git status
git checkout main && git checkout -b task/task-frontend-crud
git add src/apps/frontend/components/tasks/ && git commit -m 'Task 2 (Bonus): Add Task CRUD Frontend UI with React components'
git push -u origin task/task-frontend-crud
