from flask import Blueprint

from modules.comment.rest_api.comment_view import comment_bp


class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        # The comment_bp already has all routes defined, just register it
        # No need to call blueprint.register_blueprint here since comment_bp IS the blueprint
        return comment_bp