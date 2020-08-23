from DAO.DataBase.database import db


class RecIng(db.Model):
    __tablename__ = 'rec_ing'

    id = db.Column('id', db.Integer, primary_key=True)
    recipe = db.Column('recipe', db.Integer)
    ingredient = db.Column('ingredient', db.Integer)
