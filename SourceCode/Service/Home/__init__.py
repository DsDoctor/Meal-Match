from flask import Blueprint

home_bp = Blueprint('home', __name__)

from Service.Home import home
