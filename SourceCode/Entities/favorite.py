from DAO.DataBase.database import db


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user', db.Integer)
    recipe = db.Column('recipe', db.Integer)
