from flask import session
from Entities.recipe import Recipe
from Entities.favorite import Favorite
from Utils.get_time import time_to_str


def card(r_id):
    recipe = Recipe.query.filter_by(id=r_id).first()
    favorite = Favorite.query.filter(Favorite.recipe == recipe.id, Favorite.user == session.get('id')).first()
    if not recipe:
        return None
    else:
        res = {'id': recipe.id,
               'title': recipe.title,
               'text': recipe.describe[:200] + '...' if len(recipe.describe) > 200 else recipe.describe,
               'img_link': recipe.img_link,
               'time': time_to_str(recipe.update_time),
               'like': bool(favorite)}
        return res


if __name__ == '__main__':
    pass
