from flask import Blueprint
from flask import session
from flask import render_template
from flask_restful import Api
from Service.Recipe import recipe
from Entities.recipe import Recipe
from Entities.user import User
from Entities.rec_ing import RecIng
from Entities.ingredients import Ingredient

recipe_bp = Blueprint('recipe', __name__)
recipe_api = Api(recipe_bp)

# api corresponds to recipe steps
recipe_api.add_resource(recipe.RecSteps, '/recipe/steps')
# api corresponds to recipe type label
recipe_api.add_resource(recipe.RecTypeAPI, '/publish/rec_type')


# route for recipe detail page
@recipe_bp.route('/recipe/<rec_id>', methods=['GET'])
def rec_detail(rec_id):
    # query corresponds recipe
    dish = Recipe.query.filter_by(id=rec_id).first()
    if not dish:
        return {'res': False}, 404
    # get author
    author = User.query.filter_by(id=dish.author).first()
    # init ingredients list
    ing_res = []
    # get corresponds ingredient id
    ing_ids = RecIng.query.filter_by(recipe=dish.id).all()
    if ing_ids:
        ingredients = Ingredient.query.filter(Ingredient.id.in_([ing.ingredient for ing in ing_ids])).all()
        if ingredients:
            ing_res = [ing.name for ing in ingredients]
    # get img
    img_link = dish.img_link.split('?')[0]
    if dish.img_type != 'link':
        img_link = '/' + img_link
    # construct return date
    data = {
        'user_id': session.get('id'),
        'recipe_id': dish.id,
        'author': author.username,
        'lv': author.exp//100 + 1,
        'title': dish.title,
        'time': dish.cook_time,
        'img_link': img_link,
        'describe': dish.describe,
        'steps': dish.steps,
        'ingredients': ', '.join(ing_res),
    }
    return render_template('dish.html', **data)
