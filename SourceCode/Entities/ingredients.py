from DAO.DataBase.database import db


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
