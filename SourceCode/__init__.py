import os
import sys
from flask import Flask
from Config.config import Config
from DAO.DataBase.database import db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def create_flask_app():
    app = Flask(__name__, static_folder='Static', template_folder='UI/Templates')
    return app


def init_app():
    app = create_flask_app()

    app.config.from_object(Config)

    # connect db
    db.init_app(app)

    # Home model
    from Service.Home import home_bp
    app.register_blueprint(home_bp)

    # User model
    from Service.User import user_bp
    app.register_blueprint(user_bp)

    # Publish model
    from Service.Publish import publish_bp
    app.register_blueprint(publish_bp)

    # Search model
    from Service.Search import search_bp
    app.register_blueprint(search_bp)

    # Recipe model
    from Service.Recipe import recipe_bp
    app.register_blueprint(recipe_bp)

    # Comments model
    from Service.Comment import comments_bp
    app.register_blueprint(comments_bp)

    # Recommend model
    from Service.Recommend import recommend_bp
    app.register_blueprint(recommend_bp)

    return app
