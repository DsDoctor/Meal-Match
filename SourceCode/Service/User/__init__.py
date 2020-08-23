from flask import Blueprint
from flask import render_template
from flask_restful import Api
from Service.User import user
from flask import session
from flask import redirect
from Entities.user import User


user_bp = Blueprint('user', __name__)
user_api = Api(user_bp)

# api for user login
user_api.add_resource(user.UserLogin, '/login')
# api for user signup
user_api.add_resource(user.UserSignUp, '/signup')
# api for user reset password
user_api.add_resource(user.UserResetPW, '/reset_pw')
# api for user reset profile
user_api.add_resource(user.UserResetProfile, '/reset_profile')
# api for check email
user_api.add_resource(user.UserEmailCheck, '/email_check')
# api for email verification
user_api.add_resource(user.VerifyCheck, '/email_verify')
# api corresponds to users' favorite recipes
user_api.add_resource(user.UserFavorite, '/favorite')
# api for publish list (profile page)
user_api.add_resource(user.UserPublished, '/publish_list')
# api for user preference
user_api.add_resource(user.UserPrefer, '/user/pre')


@user_bp.route('/profile')
def user():
    u = User.query.filter_by(id=session.get('id')).first()
    data = {'username': u.username,
            'email': u.email,
            'lv': u.exp//100 + 1,
            'exp': f'{u.exp % 100}/100',
            'exp_value': u.exp % 100}
    return render_template('profile.html', **data)


@user_bp.route('/signup', methods=['GET'])
def setup():
    return render_template('signup.html')


@user_bp.route('/forgot_pw')
def forgot_pw():
    return render_template('forgot_password.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
