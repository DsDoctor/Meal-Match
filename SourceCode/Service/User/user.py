from flask_restful import Resource
from flask import request
from flask import session
from DAO.DataBase.database import db
from Entities.user import User
from Entities.rec_type import RecType
from Entities.favorite import Favorite
from Entities.recipe import Recipe
from Entities.user_pre import UserPre
from Utils.gen_card import card
from Utils.get_time import time_now, check_exp
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
import re


def verify_code(code, email):
    if not code:
        return False
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email_code = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    for s in ['.', '_', '-']:
        email_code = email_code.replace(s, '')
    if code.upper() not in email_code.upper():
        return False
    return True


def init_preference(user):
    user_p = UserPre.query.filter_by(user=user.id).all()
    preferences = RecType.query.filter(RecType.id.in_([p.pre for p in user_p])).all()
    pre_list = []
    for p in preferences:
        pre_list.append({
            'id': p.id,
            'f_name': p.name
        })
    session['filter'] = str(pre_list)


class UserLogin(Resource):
    def post(self):
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            username = email
            users = User.query.filter_by(username=username).all()
            for user in users:
                if check_password_hash(user.password, password):
                    break
            else:
                return jsonify({'res': False})
        session['user'] = user.username
        session['id'] = user.id
        session.permanent = True if request.form.get("remember") == 'true' else False
        user.visit_time = time_now()
        user = check_exp(user)
        # init user preference
        init_preference(user)
        db.session.commit()
        return jsonify({'res': True})


class UserSignUp(Resource):
    def post(self):
        email = request.form.get('email')
        username = request.form.get('username')
        if not username:
            username = email.split('@')[0]
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            return {'res': False}, 400
        code = request.form.get('verify')
        if not verify_code(code, email):
            return {'res': False}, 400
        preferences = eval(request.form.get('cat'))
        _password = generate_password_hash(password1)
        user = User(username=username, password=_password, email=email, visit_time=time_now())
        db.session.add(user)
        db.session.commit()
        user_pre = [int(re.findall(r'[0-9]+', p)[0]) for p in preferences]
        for p in user_pre:
            pre = UserPre(user=user.id, pre=p)
            db.session.add(pre)
        db.session.commit()
        session['user'] = username
        session['id'] = user.id
        init_preference(user)
        return jsonify({'res': True})


class UserResetPW(Resource):
    def post(self):
        email = request.form.get('email')
        new_pw1 = request.form.get('password1')
        new_pw2 = request.form.get('password2')
        code = request.form.get('verify')
        if new_pw1 != new_pw2:
            return {'res': False}, 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return {'res': False}, 400
        if not verify_code(code, email):
            return {'res': False}, 400
        user.password = generate_password_hash(new_pw1)
        db.session.commit()
        return jsonify({'res': True})


class UserResetProfile(Resource):
    def post(self):
        user_id = session.get('id')
        username = request.form.get('username')
        email = request.form.get('email')
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'res': False}, 400
        user.username = username
        user.email = email
        preferences = eval(request.form.get('cat'))
        preferences = [int(re.findall(r'[0-9]+', p)[0]) for p in preferences]
        user_pre = UserPre.query.filter_by(user=user_id).all()
        # 之前的pre 不在新提交的pre里 删掉之前的pre
        for p in user_pre:
            if p.pre not in preferences:
                db.session.delete(p)
        # 新提交的pre 不在已经存下的pre里 则添加
        user_pre = UserPre.query.filter_by(user=user_id).all()
        user_pre = [p.pre for p in user_pre]
        for p in preferences:
            if p not in user_pre:
                pre = UserPre(user=user_id, pre=p)
                db.session.add(pre)
        db.session.commit()
        session['user'] = username
        init_preference(user)
        return {'res': True}


class UserEmailCheck(Resource):
    def get(self):
        email = request.args.get('email')
        method = request.args.get('method')
        res = re.findall(r'([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', email if email else '')
        if not res:
            return {'msg': 'Please check your email.'}, 400
        email = res[0]
        signed = User.query.filter_by(email=email).first()
        if signed:
            if method == 'signup':
                return {'msg': 'The email address has been registered.'}, 400
            else:
                return {'msg': 'Congratulation! The email address is Valid'}
        else:
            if method == 'reset':
                return {'msg': 'The email address has not registered yet.'}, 400
            else:
                return {'msg': 'Congratulation! The email address is Valid'}


class UserPrefer(Resource):
    def get(self):
        res = []
        user_pre = [p.pre for p in UserPre.query.filter_by(user=session.get('id')).all()]
        pre = RecType.query.all()[26:]
        for p in pre:
            res.append({
                'id': p.id,
                'cat': p.name.title(),
                'checked': True if p.id in user_pre else False
            })
        return jsonify(res)


class VerifyCheck(Resource):
    def get(self):
        email = request.args.get('email')
        v_code = request.args.get('verify')
        if verify_code(v_code, email):
            return {'msg': 'Verified!'}
        else:
            return {'msg': 'Failed to verify.'}, 400


class UserFavorite(Resource):
    def get(self):
        data = []
        user = session.get('id')
        f_list = Favorite.query.filter_by(user=user).all()
        if not f_list:
            return {'res': False}, 400
        for f in f_list:
            recipe = Recipe.query.filter_by(id=f.recipe).first()
            data.append(card(recipe.id))
        return jsonify(data)

    def post(self):
        user = session.get('id')
        r_id = request.form.get('id')
        f = Favorite.query.filter_by(user=user, recipe=r_id).first()
        if f or not user:
            return {"res": False}, 400
        f = Favorite(user=user, recipe=r_id)
        recipe = Recipe.query.filter_by(id=r_id).first()
        recipe.like += 1
        db.session.add(f)
        user = User.query.filter_by(id=user).first()
        if user.max_exp <= 30:
            user.exp += 1
            user.max_exp += 1
        db.session.commit()
        return {'res': True}

    def delete(self):
        user = session.get('id')
        r_id = request.form.get('id')
        if not user or not r_id:
            return {"res": False}, 400
        f = Favorite.query.filter_by(user=user, recipe=r_id).first()
        recipe = Recipe.query.filter_by(id=r_id).first()
        recipe.like -= 1
        db.session.delete(f)
        db.session.commit()
        return {"res": True}


class UserPublished(Resource):
    def get(self):
        data = []
        user = session.get('id')
        r_list = Recipe.query.filter_by(author=user).all()
        if not r_list:
            return {'res': False}, 400
        for recipe in r_list:
            data.append(card(recipe.id))
        return jsonify(data)
