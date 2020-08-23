from flask import Blueprint
from flask_restful import Api
from Service.Comment import comment

comments_bp = Blueprint('comments', __name__)
comments_api = Api(comments_bp)

comments_api.add_resource(comment.CommentsApi, '/comments')
