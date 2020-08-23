import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    # secret key
    SECRET_KEY = 'COMP9900PROJECT-TheAvengers'
    SECURITY_PASSWORD_SALT = 'COMP9900PROJECT-TheAvengers-email'

    # session delay
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # database config
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'DAO/DataBase/database.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_ECHO = False

    # MAIL_SERVER = 'smtp.office365.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'MealMatch@outlook.com'
    # MAIL_PASSWORD = 'COMP9900meal_match'

    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    MAIL_USERNAME = 'z5171466@ad.unsw.edu.au'
    MAIL_PASSWORD = 'wanmeids721DOOM'
