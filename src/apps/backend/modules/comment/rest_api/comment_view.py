from flask import Blueprint, jsonify, request
from datetime import datetime
from modules.comment.comment_service import CommentService
from modules.comment.types import (
    CreateCommentParams,
    UpdateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetCommentsByTaskParams,
)

comment_bp = Blueprint('comment', __name__, url_prefix='/api/v1/comments')

@comment_bp.route('', methods=['POST'])
def create_comment():
    """Create a new comment"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['task_id', 'account_id', 'content']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    params = CreateCommentParams(
        task_id=data['task_id'],
        account_id=data['account_id'],
        content=data['content']
    )
    
    comment = CommentService.create_comment(params)
    return jsonify({
        'id': comment.id,
        'task_id': comment.task_id,
        'account_id': comment.account_id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat() if comment.updated_at else None,
    }), 201

@comment_bp.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a specific comment"""
    task_id = request.args.get('task_id')
    account_id = request.args.get('account_id')
    
    if not task_id or not account_id:
        return jsonify({'error': 'Missing task_id or account_id'}), 400
    
    params = GetCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id
    )
    
    comment = CommentService.get_comment(params)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    return jsonify({
        'id': comment.id,
        'task_id': comment.task_id,
        'account_id': comment.account_id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat() if comment.updated_at else None,
    })

@comment_bp.route('/<comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update a comment"""
    data = request.get_json()
    
    if not data or 'content' not in data:
        return jsonify({'error': 'Missing content field'}), 400
    
    task_id = request.args.get('task_id')
    account_id = request.args.get('account_id')
    
    if not task_id or not account_id:
        return jsonify({'error': 'Missing task_id or account_id'}), 400
    
    params = UpdateCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id,
        content=data['content']
    )
    
    comment = CommentService.update_comment(params)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    return jsonify({
        'id': comment.id,
        'task_id': comment.task_id,
        'account_id': comment.account_id,
        'content': comment.content,
        'created_at': comment.created_at.isoformat(),
        'updated_at': comment.updated_at.isoformat() if comment.updated_at else None,
    })

@comment_bp.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment"""
    task_id = request.args.get('task_id')
    account_id = request.args.get('account_id')
    
    if not task_id or not account_id:
        return jsonify({'error': 'Missing task_id or account_id'}), 400
    
    params = DeleteCommentParams(
        comment_id=comment_id,
        task_id=task_id,
        account_id=account_id
    )
    
    if not CommentService.delete_comment(params):
        return jsonify({'error': 'Comment not found'}), 404
    
    return '', 204

@comment_bp.route('/task/<task_id>', methods=['GET'])
def get_task_comments(task_id):
    """Get all comments for a task"""
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({'error': 'Missing account_id'}), 400
    
    params = GetCommentsByTaskParams(
        task_id=task_id,
        account_id=account_id
    )
    
    comments = CommentService.get_comments_by_task(params)
    return jsonify([
        {
            'id': c.id,
            'task_id': c.task_id,
            'account_id': c.account_id,
            'content': c.content,
            'created_at': c.created_at.isoformat(),
            'updated_at': c.updated_at.isoformat() if c.updated_at else None,
        }
        for c in comments
    ])
