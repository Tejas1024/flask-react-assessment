from bson.objectid import ObjectId
from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.comment_util import CommentUtil
from modules.comment.types import Comment, GetCommentParams, GetCommentsByTaskParams
from typing import List

class CommentReader:
    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        comment_bson = CommentRepository.collection().find_one({
            "_id": ObjectId(params.comment_id),
            "task_id": params.task_id,
            "account_id": params.account_id,
            "active": True
        })
        
        if comment_bson is None:
            raise CommentNotFoundError(comment_id=params.comment_id)
        
        return CommentUtil.convert_comment_bson_to_comment(comment_bson)

    @staticmethod
    def get_comments_by_task(*, params: GetCommentsByTaskParams) -> List[Comment]:
        filter_query = {
            "task_id": params.task_id,
            "account_id": params.account_id,
            "active": True
        }
        
        cursor = CommentRepository.collection().find(filter_query).sort([
            ("created_at", -1),
            ("_id", -1)
        ])
        
        comments_bson = list(cursor)
        return [CommentUtil.convert_comment_bson_to_comment(c) for c in comments_bson]from bson.objectid import ObjectId
from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.comment_util import CommentUtil
from modules.comment.types import Comment, GetCommentParams, GetCommentsByTaskParams
from typing import List

class CommentReader:
    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        comment_bson = CommentRepository.collection().find_one({
            "_id": ObjectId(params.comment_id),
            "task_id": params.task_id,
            "account_id": params.account_id,
            "active": True
        })
        
        if comment_bson is None:
            raise CommentNotFoundError(comment_id=params.comment_id)
        
        return CommentUtil.convert_comment_bson_to_comment(comment_bson)

    @staticmethod
    def get_comments_by_task(*, params: GetCommentsByTaskParams) -> List[Comment]:
        filter_query = {
            "task_id": params.task_id,
            "account_id": params.account_id,
            "active": True
        }
        
        cursor = CommentRepository.collection().find(filter_query).sort([
            ("created_at", -1),
            ("_id", -1)
        ])
        
        comments_bson = list(cursor)
        return [CommentUtil.convert_comment_bson_to_comment(c) for c in comments_bson]
