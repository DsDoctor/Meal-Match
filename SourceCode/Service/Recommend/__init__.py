from flask import Blueprint
from flask_restful import Api
from Service.Recommend import recommend

recommend_bp = Blueprint('recommend', __name__)
recommend_api = Api(recommend_bp)

# recommend api for recommend ingredient type
recommend_api.add_resource(recommend.RecIngType, '/recommend/ing_type')
# recommend api for recommend ingredient to running list
# (including identify input ingredient and next ingredient)
recommend_api.add_resource(recommend.RecIngToList, '/recommend/ing_to_list')
# recommend api for recommend ingredient challenge (ingredient set)
recommend_api.add_resource(recommend.RecIngSet, '/recommend/ing_set')

