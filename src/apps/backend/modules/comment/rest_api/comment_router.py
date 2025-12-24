from flask import Blueprint

from modules.comment.rest_api.comment_view import comment_bp


class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        # Register the comment blueprint routes
        blueprint.register_blueprint(comment_bp)
        return blueprint
