from flask_restful import Resource
from flask import request
from flask import jsonify
from Entities.recipe import Recipe
from Entities.rec_type import RecType
from Entities.relation_rec_type import RelRecType


class RecSteps(Resource):
    # get recipe steps
    def get(self):
        # get recipe id
        r_id = request.args.get('id')
        if not r_id:
            return {'res': False}, 400
        recipe = Recipe.query.filter_by(id=r_id).first()
        return jsonify([s for s in recipe.steps.split('\n')])


class RecTypeAPI(Resource):
    # get the list of recipe type (meal type)
    def get(self):
        res = []
        rec_types = RecType.query.all()
        r_id = request.args.get('r_id')
        check_list = []
        if r_id:
            check_list = [r.t_id for r in RelRecType.query.filter_by(r_id=r_id).all()]
        for rec_type in rec_types[3:]:
            res.append({
                'id': rec_type.id,
                'cat': rec_type.name.title(),
                'checked': True if rec_type.id in check_list else False
            })
        return jsonify(res)
