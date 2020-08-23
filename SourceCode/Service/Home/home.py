from Service.Home import home_bp
from flask import render_template
from flask import session
from DAO.DataBase.database import db
from Entities.user import User
from Entities.recipe import Recipe
from Entities.favorite import Favorite
from Utils.get_time import time_to_str, check_exp
from Utils.string_process import cut_length


@home_bp.route('/')
def home():
    data = {}
    r_id = []
    # query 3 type of sorting from db
    res = [Recipe.query.order_by(Recipe.update_time.desc()).limit(9).all(),
           Recipe.query.order_by(Recipe.like.desc()).limit(9).all(),
           Recipe.query.order_by(Recipe.cook_time).limit(9).all()]
    # select recipe showing on home page
    for j in range(3):
        i = 0
        while i < 3:
            recipe = res[j].pop(0)
            if recipe.id in r_id:
                continue
            data[f'card{i+(1+3*j)}_id'] = recipe.id
            data[f'card{i+(1+3*j)}_title'] = recipe.title
            data[f'card{i+(1+3*j)}_img'] = recipe.img_link
            data[f'card{i+(1+3*j)}_time'] = time_to_str(recipe.update_time)
            data[f'card{i+(1+3*j)}_text'] = cut_length(recipe.describe, 200)
            favorite = Favorite.query.filter(Favorite.recipe == recipe.id, Favorite.user == session.get('id')).first()
            data[f'card{i+(1+3*j)}_icon'] = 'star-fill.svg' if favorite else 'star.svg'
            i += 1
            r_id.append(recipe.id)
    # check login
    user = session.get('user')
    user = User.query.filter_by(username=user).first()
    if user:
        user = check_exp(user)
        db.session.commit()
        data['login'] = 'true'
        data['user'] = user.username
    else:
        session.clear()
        data['login'] = 'false'
        data['user'] = ''
    return render_template('index.html', **data)
