from dataclasses import asdict
from flask import Blueprint, jsonify, request
from flask.typing import ResponseReturnValue

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentBadRequestError
from modules.comment.types import (
    CreateCommentParams,
    UpdateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetCommentsByTaskParams,
)

comment_bp = Blueprint('comments', __name__, url_prefix='/api/accounts/<account_id>/tasks/<task_id>/comments')

@comment_bp.route('', methods=['POST'])
@access_auth_middleware
def create_comment(account_id: str, task_id: str) -> ResponseReturnValue:
    data = request.get_json()
    
    if not data or 'content' not in data:
        raise CommentBadRequestError('Content is required')
    
    params = CreateCommentParams(
        task_id=task_id,
        account_id=account_id,
        content=data['content']
    )
    
    comment = CommentService.create_comment(params=params)
    return jsonify(asdict(comment)), 201

@comment_bp.route('/<comment_id>', methods=['GET'])
@access_auth_middleware
def get_comment(account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
    params = GetCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id
    )
    
    comment = CommentService.get_comment(params=params)
    return jsonify(asdict(comment)), 200

@comment_bp.route('/<comment_id>', methods=['PATCH'])
@access_auth_middleware
def update_comment(account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
    data = request.get_json()
    
    if not data or 'content' not in data:
        raise CommentBadRequestError('Content is required')
    
    params = UpdateCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id,
        content=data['content']
    )
    
    comment = CommentService.update_comment(params=params)
    return jsonify(asdict(comment)), 200

@comment_bp.route('/<comment_id>', methods=['DELETE'])
@access_auth_middleware
def delete_comment(account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
    params = DeleteCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id
    )
    
    CommentService.delete_comment(params=params)
    return '', 204

@comment_bp.route('', methods=['GET'])
@access_auth_middleware
def get_task_comments(account_id: str, task_id: str) -> ResponseReturnValue:
    params = GetCommentsByTaskParams(
        task_id=task_id,
        account_id=account_id
    )
    
    comments = CommentService.get_comments_by_task(params=params)
    return jsonify([asdict(c) for c in comments]), 200