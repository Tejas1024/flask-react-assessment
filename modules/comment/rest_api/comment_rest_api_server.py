from flask import Blueprint
from modules.comment.rest_api.comment_view import comment_bp


class CommentRestApiServer:
    @staticmethod
    def create() -> Blueprint:
        # Return the comment_bp directly since it already has all routes
        return comment_bp
